#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
python "$HERE/audit_physical.py" --part ground > "$HERE/logs/ground.log" 2>&1
python "$HERE/audit_physical.py" --part translation > "$HERE/logs/translation.log" 2>&1
python "$HERE/audit_paths.py" > "$HERE/logs/paths.log" 2>&1
python "$HERE/audit_certificates.py" > "$HERE/logs/certificates.log" 2>&1
cat "$HERE/logs/paths.log" "$HERE/logs/certificates.log"
