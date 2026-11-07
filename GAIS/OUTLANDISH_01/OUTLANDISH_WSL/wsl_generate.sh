#!/usr/bin/env bash
# Safe preview-by-default native Debian y-cruncher runner.
# Sources reside on E:, only attempts/swap/text/reports reside on ext4 (T: VHDX).
set -euo pipefail
umask 077

CONSTANT=""; DIGITS=""; EXECUTE=0; ACK=""; TD=1; MEMORY="4g"; MODE="swap"; BENCHMARK_NO_VERIFY=0
EXE="$HOME/outlandish-test/y-cruncher v0.8.7.9547-static/y-cruncher"
WORK="$HOME/outlandish-work"
usage(){ cat <<'EOF'
Usage: bash wsl_generate.sh --constant {pi|phi|e|log2|gamma|lemniscate} --digits N
       [--mode swap|ram] [--memory 4g] [--td 1] [--work-root PATH]
       [--ycruncher PATH] [--benchmark-no-verify] [--run] [--ack-large-run N]

Defaults to PREVIEW: does not launch y-cruncher or make directories.
For >=1e9, --run also needs --ack-large-run N (repeat exact digit count).
Resource estimates must be inspected before authorising a large run.
Verification is ON by default. --benchmark-no-verify is ONLY for throwaway
performance benchmarks; unverified decimal digits are NOT production eligible.
EOF
}
while [[ $# -gt 0 ]]; do
    case "$1" in
        --constant) CONSTANT=${2:?}; shift 2;;
        --digits) DIGITS=${2:?}; shift 2;;
        --mode) MODE=${2:?}; shift 2;;
        --memory) MEMORY=${2:?}; shift 2;;
        --td) TD=${2:?}; shift 2;;
        --work-root) WORK=${2:?}; shift 2;;
        --ycruncher) EXE=${2:?}; shift 2;;
        --benchmark-no-verify) BENCHMARK_NO_VERIFY=1; shift;;
        --run) EXECUTE=1; shift;;
        --ack-large-run) ACK=${2:?}; shift 2;;
        --help|-h) usage; exit 0;;
        *) echo "Unknown option: $1" >&2; usage >&2; exit 2;;
    esac
done
case "$CONSTANT" in
    pi) YCONST=pi;; phi) YCONST=goldenratio;; e) YCONST=e;;
    log2) YCONST=log:2;; gamma) YCONST=gamma;; lemniscate) YCONST=lemniscate;;
    *) echo 'Invalid --constant' >&2; exit 2;;
esac
[[ "$DIGITS" =~ ^[0-9]+$ ]] && (( DIGITS >= 33 && DIGITS <= 100000000000 )) || { echo 'Invalid --digits (33..1e11)' >&2; exit 2; }
[[ "$TD" =~ ^[0-9]+$ ]] && (( TD >= 1 && TD <= 4 )) || { echo 'TD must be 1..4' >&2; exit 2; }
[[ "$MODE" == swap || "$MODE" == ram ]] || { echo 'Invalid mode' >&2; exit 2; }
[[ "$MEMORY" =~ ^[1-9][0-9]*[gGmM]$ ]] || { echo 'Memory needs format 4g or 256m' >&2; exit 2; }
[[ "$WORK" == "$HOME"/* ]] || { echo 'Work root must be inside Linux home (ext4)' >&2; exit 2; }
[[ -f "$EXE" ]] || { echo "y-cruncher executable missing: $EXE" >&2; exit 2; }
[[ "$MODE" == swap || "$DIGITS" -lt 5000000000 ]] || { echo 'RAM >=5e9 refused' >&2; exit 2; }
FRAMEWORK=taskqueue; [[ "$TD" == 1 ]] && FRAMEWORK=none
VERIFY_FLAG=1; VERIFY_LABEL=ON; RUN_CLASS=VERIFIED_GENERATION
if (( BENCHMARK_NO_VERIFY )); then
    VERIFY_FLAG=0; VERIFY_LABEL=OFF; RUN_CLASS=BENCHMARK_UNVERIFIED
fi
ATTEMPT="${CONSTANT}_${DIGITS}_$(date -u +%Y%m%dT%H%M%SZ)_$RANDOM"
FOLDER="$WORK/$ATTEMPT"
SWAP="$FOLDER/swap"
CMD=("$EXE" custom "$YCONST" "-dec:$((DIGITS-1))" '-hex:0' '-od:1' '-compress:0' "-verify:$VERIFY_FLAG" "-mode:$MODE" "-TD:$TD" "-PF:$FRAMEWORK")
if [[ "$MODE" == swap ]]; then CMD+=("-M:$MEMORY" '-swap:raid0' "$SWAP"); fi
printf 'CONSTANT=%s TOTAL_DIGITS_INCLUDING_INTEGER=%s\n' "$CONSTANT" "$DIGITS"
printf 'EXT4_WORK=%s\nMODE=%s TD=%s FRAMEWORK=%s MEMORY_CAP=%s VERIFY_OUTPUT=%s RUN_CLASS=%s\n' "$FOLDER" "$MODE" "$TD" "$FRAMEWORK" "$MEMORY" "$VERIFY_LABEL" "$RUN_CLASS"
if (( BENCHMARK_NO_VERIFY )); then
    echo 'WARNING: BENCHMARK ONLY. y-cruncher base-conversion/output verification DISABLED.'
    echo 'WARNING: Output is NOT ELIGIBLE for packed conversion, registration or production.'
fi
printf 'COMMAND (display only): '; printf '%q ' "${CMD[@]}"; echo
if (( !EXECUTE )); then echo 'PREVIEW ONLY: no computation, files or directories created.'; exit 0; fi
if (( DIGITS >= 1000000000 )) && [[ "$ACK" != "$DIGITS" ]]; then
    echo "REFUSED: for >=1e9, provide --ack-large-run $DIGITS after owner resource review" >&2
    exit 2
fi
[[ ! -e "$FOLDER" ]] || { echo 'Attempt folder exists' >&2; exit 2; }
mkdir -p -- "$SWAP"
cd "$FOLDER"
printf 'RUN_CLASS=%s VERIFY_OUTPUT=%s\n' "$RUN_CLASS" "$VERIFY_LABEL" | tee -a run.log
printf 'START %s\n' "$(date -u --iso-8601=seconds)" | tee -a run.log
# The y-cruncher process is a foreground child, not a detached long-running job.
set +e
"${CMD[@]}" 2>&1 | tee -a run.log
status=${PIPESTATUS[0]}
set -e
printf 'EXIT=%d FINISH=%s\n' "$status" "$(date -u --iso-8601=seconds)" | tee -a run.log
exit "$status"
