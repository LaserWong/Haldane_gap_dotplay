#!/bin/bash
# Usage: check_only.sh ORIG|FULL TAG GAP DIGITS  (certificate_TAG.json already written by produce_fast.py)
set -o pipefail
MODE=$1 TAG=$2 GAP=$3 D=$4
AU=/workspace/haldane_chat_bundle/runs/watertight/auditor; P=/workspace/haldane_chat_bundle/runs/push_bound; OUT=$P/certs/$TAG
RR=$AU/orig_audit/research_20261010
cd $AU; T0=$(date +%s)
if [ $MODE = ORIG ]; then
  ( time CPU_LIMIT=${CPU_LIMIT:-590} DIGITS=$D python3 $P/run_orig_logic_cpu.py scalar $TAG ) > $OUT/2_scalar_check_ORIGINAL_cpu${CPU_LIMIT:-590}.log 2>&1 || { echo SCALAR_FAIL; exit 1; }
else
  ( time AUDIT_FULL_R68=1 AUDIT_DIGITS=$D AUDIT_CERT=certificate_$TAG.json AUDIT_OUT=ORIG_scalar_results_$TAG.json python3 run_patched.py ) > $OUT/2_scalar_check_PATCHED_FULL.log 2>&1 || { echo SCALAR_FAIL; exit 1; }
fi
T1=$(date +%s)
TAG=$TAG GAP=$GAP python3 produce_allsizes_orig.py > $OUT/3_allsizes_producer.log 2>&1 && python3 run_orig_logic.py allsizes $TAG $GAP > $OUT/4_allsizes_check_ORIGINAL.log 2>&1 || { echo ALLSIZES_FAIL; exit 1; }
T2=$(date +%s)
cp $RR/uniform_smaller_second_initialization/certificate_$TAG.json $RR/uniform_smaller_second_initialization_review/ORIG_scalar_results_$TAG.json $RR/uniform_gap_0248_all_sizes_review/ORIG_results_$TAG.json $OUT/
echo "{\"mode\":\"$MODE\",\"tag\":\"$TAG\",\"gap\":\"$GAP\",\"digits\":$D,\"scalar_check_wall_s\":$((T1-T0)),\"allsizes_wall_s\":$((T2-T1))}" | tee $OUT/SUMMARY.json
