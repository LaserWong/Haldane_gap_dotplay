#!/bin/bash
# Usage: certify.sh ORIG|FULL TAG GAP W DIGITS
# ORIG: producer (Z_{2n}>1 recipe) -> ORIGINAL git-HEAD audit_scalar.py (run_orig_logic.py; substitutions only file
#       names/affinity/rounding grid B) -> producer of all-sizes rows -> ORIGINAL audit.py (all L>=2).
# FULL: producer with AUDIT_FULL_R68=1 -> PATCHED audit_scalar.py (seal12 diff, FULL Jensen forcing) -> ORIGINAL audit.py.
set -eo pipefail
MODE=$1 TAG=$2 GAP=$3 W=$4 D=$5
AU=/workspace/haldane_chat_bundle/runs/watertight/auditor
REV=$AU/orig_audit/research_20261010/uniform_smaller_second_initialization_review
OUT=/workspace/haldane_chat_bundle/runs/push_bound/certs/$TAG; mkdir -p $OUT
cd $AU
T0=$(date +%s)
if [ $MODE = ORIG ]; then
  env -u AUDIT_FULL_R68 AUDIT_DIGITS=$D W=$W GAP=$GAP AUDIT_CERT=certificate_$TAG.json python3 produce_patchedprefix.py | tee $OUT/1_producer.log
  DIGITS=$D python3 run_orig_logic.py scalar $TAG | tee $OUT/2_scalar_check_ORIGINAL.log
else
  AUDIT_FULL_R68=1 AUDIT_DIGITS=$D W=$W GAP=$GAP AUDIT_CERT=certificate_$TAG.json python3 produce_patchedprefix.py | tee $OUT/1_producer.log
  AUDIT_FULL_R68=1 AUDIT_DIGITS=$D AUDIT_CERT=certificate_$TAG.json AUDIT_OUT=ORIG_scalar_results_$TAG.json python3 run_patched.py | tee $OUT/2_scalar_check_PATCHED_FULL.log
fi
T1=$(date +%s)
TAG=$TAG GAP=$GAP python3 produce_allsizes_orig.py | tee $OUT/3_allsizes_producer.log
python3 run_orig_logic.py allsizes $TAG $GAP | tee $OUT/4_allsizes_check_ORIGINAL.log
T2=$(date +%s)
cp $AU/orig_audit/research_20261010/uniform_smaller_second_initialization/certificate_$TAG.json $OUT/
cp $REV/ORIG_scalar_results_$TAG.json $OUT/ 2>/dev/null || true
cp $AU/orig_audit/research_20261010/uniform_gap_0248_all_sizes_review/ORIG_results_$TAG.json $OUT/ 2>/dev/null || true
echo "{\"mode\":\"$MODE\",\"tag\":\"$TAG\",\"gap\":\"$GAP\",\"W\":$W,\"digits\":$D,\"scalar_wall_s\":$((T1-T0)),\"allsizes_wall_s\":$((T2-T1))}" | tee $OUT/SUMMARY.json
