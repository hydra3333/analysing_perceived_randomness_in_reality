#!/bin/sh
# Verify files at a commit by hashing the Git blobs (LF), never the working tree.
# Usage: sh 01_verify_commit_hashes.sh <repo> <commit> <path> [<path> ...]
repo=$1; commit=$2; shift 2
for p in "$@"; do printf "%s  " "$(git -C "$repo" show "$commit:$p" | sha256sum | cut -c1-64)"; echo "$p"; done
# A file you hold with CRLF endings: compare its LF form with
#   sed 's/\r$//' file | sha256sum
