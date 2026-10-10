#!/bin/sh
set -eu
cd "$(dirname "$0")"
python independent_physical.py > independent_physical.log
g++ -O3 -std=c++17 independent_contract.cpp -lgmpxx -lgmp -o independent_contract
./independent_contract inputs/sources.txt > independent_contractions.out 2> independent_contractions.log
g++ -O3 -std=c++17 independent_ground.cpp -lgmpxx -lgmp -o independent_ground
./independent_ground inputs/mps_blocks.txt > independent_ground.out 2> independent_ground.log
python independent_scalar.py > independent_scalar.log
python regressions.py > regressions.log
