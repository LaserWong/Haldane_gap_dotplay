#!/bin/bash
run(){ m=$1; tn=$2; td=$3; tag=$4
 for r in 1 -1; do for f in 1 -1; do echo "=== $tag $m $r $f $tn/$td ==="; python3 cert_ring_block.py $m $r $f $tn $td 2e-6 | python3 -c "import json,sys; d=json.loads(sys.stdin.read()); print({k:d.get(k) for k in ['n','r','f','t','db','kb','CERTIFIED','reason','lam_min_AstarU_lower','E_build','rho','F2']})"; done; done; }
run 3 79 100 CERT; run 3 81 100 NEG
run 4 7975 100000 CERT; run 4 7977 100000 NEG
run 5 2121 10000 CERT; run 5 2122 10000 NEG
run 6 959 10000 CERT; run 6 960 10000 NEG
run 7 1517 10000 CERT; run 7 1518 10000 NEG
echo ALLDONE
