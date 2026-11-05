#!/bin/bash
# full pipeline for one block KEY; each stage a separate process (box: ~600 s CPU/process)
cd "$(dirname "$0")"; K=$1; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
[ -f enc/$K.json ] && exit 0
run(){ timeout 595 python3 chunked.py "$@" >> logs/$K.log 2>&1 || { echo "FAIL $*" >> logs/$K.log; exit 1; }; }
run eig $K
for I in 0 1 2 3; do for J in $(seq $I 3); do run gram $K $I $J; done; done
for c in 0 1 2 3; do run resid $K $c; done
run finish $K && rm -f work/${K}_V?.npy && echo "DONE $K" >> logs/$K.log
