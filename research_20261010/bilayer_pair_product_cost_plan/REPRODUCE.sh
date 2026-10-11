#!/bin/sh
set -eu
cd "$(dirname "$0")"
ulimit -t 60
ulimit -v 262144
out=$(mktemp)
trap 'rm -f "$out"' EXIT
taskset -c 6 python check_geometry.py > "$out"
cmp geometry.json "$out"
echo 'PASS: exact geometry and rational bounds reproduced; no physical state contraction'
