#!/bin/sh
set -eu
cd "$(dirname "$0")"
python independent_physical.py > independent_physical.log
g++ -O3 -std=c++17 independent_contract.cpp -lgmpxx -lgmp -o independent_contract
./independent_contract inputs/sources.txt > independent_contractions.out 2> independent_contractions.log
python independent_scalar.py > independent_scalar.log
python independent_conditional.py > independent_conditional.log
python regressions.py > regressions.log
