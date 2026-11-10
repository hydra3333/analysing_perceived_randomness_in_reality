#!/bin/sh
# Negative checks of the DRAFT scaffold; each must STOP. Usage: neg_smoke.sh MIRROR PKGDIR WORK PYTHON
set -u
MIRROR="$1"; PKGSRC="$2"; W="$3"; PY="$4"
fresh() { rm -rf "$W"; mkdir -p "$W"; cp -r "$PKGSRC" "$W/stage"; git clone -q "$MIRROR" "$W/repo"; R="$W/repo"; PKG="$W/stage"; }
expect_stop() { label="$1"; shift; out=$("$@" 2>&1); rc=$?; if [ $rc -ne 0 ]; then echo "STOPPED as required: $label -> $(echo "$out" | grep -E 'STOP|FAIL' | head -1 | cut -c1-150)"; else echo "NEGATIVE FAILED (did not stop): $label"; fi; }
fresh; printf 'x' >> "$PKG/repo_overlay/src/methods/_common/contract_vocab.py"
expect_stop "damaged package file, copy gate" "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part gate --repo "$R"
echo "    repo unchanged: $(git -C $R status --short | wc -l) status lines"
expect_stop "damaged package file, PRE" "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase pre
fresh; printf 'stray\n' > "$R/stray.txt"
expect_stop "untracked file at PRE" "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase pre
fresh; "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part gate --repo "$R" >/dev/null; "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part rest --repo "$R" >/dev/null
rm "$R/src/methods/_common/owner_records.py"
expect_stop "missing new file at POST (R-008 wording)" "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase post
fresh; "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part gate --repo "$R" >/dev/null; "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part rest --repo "$R" >/dev/null
printf 'extra\n' > "$R/src/methods/_common/extra.py"
expect_stop "extra file at POST" "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase post
rm "$R/src/methods/_common/extra.py"; printf '#\n' >> "$R/src/methods/_common/contract_task.py"
expect_stop "wrong bytes at POST" "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase post
fresh; "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part gate --repo "$R" >/dev/null
expect_stop "copy gate twice (targets no longer at base)" "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part gate --repo "$R"
fresh; mkdir -p "$R/src/methods/_common/contract_data"; printf 'not ours\n' > "$R/src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt"
expect_stop "remove barrier P with foreign content" "$PY" -I -B "$PKG/MHUPA_COPY.py" barrier --remove P --repo "$R"
echo "    foreign P still present: $(test -f $R/src/methods/_common/contract_data/INSTALL_IN_PROGRESS.txt && echo yes || echo NO)"
expect_stop "create barrier P when present" "$PY" -I -B "$PKG/MHUPA_COPY.py" barrier --create P --repo "$R"
fresh; "$PY" -I -c "
import json,sys; p=sys.argv[1]; m=json.load(open(p)); g=m['gate_files']; g[0]='../outside.py'; m['new']['../outside.py']='0'*64; open(p,'w').write(json.dumps(m))" "$PKG/PACKAGE_MANIFEST_MHUP_A.json"
expect_stop "path traversal in manifest (copy)" "$PY" -I -B "$PKG/MHUPA_COPY.py" copy --part gate --repo "$R"
expect_stop "altered manifest (verifier)" "$PY" -I -B "$PKG/VERIFY_MHUP_A.py" --repo "$R" --phase pre
