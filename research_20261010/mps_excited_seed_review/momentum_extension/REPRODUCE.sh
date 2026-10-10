#!/bin/sh
set -eu
cd "$(dirname "$0")"
# Run on a copy to preserve immutable recorded outputs. Suggested: taskset -c 1.
python build_independent.py > independent_build.log
g++ -O3 -std=c++17 independent_channels.cpp -lgmpxx -lgmp -o independent_channels
./independent_channels single_site_sources.txt 6 0 1 2 3 4 5 > independent_n6.out 2> independent_n6.log
./independent_channels single_site_sources.txt 24 0 12 > independent_n24_benchmark.out 2> independent_n24_benchmark.log
./independent_channels single_site_sources.txt 24 1 2 3 4 5 6 7 8 9 10 11 > independent_n24_remaining.out 2> independent_n24_remaining.log
./independent_channels single_site_sources.txt 2 0 1 > independent_n2.out 2> independent_n2.log
./independent_channels single_site_sources.txt 4 0 1 2 3 > independent_n4.out 2> independent_n4.log
python independent_fourier.py > independent_fourier.log
python independent_singlet.py > independent_singlet.log
python independent_scalar.py 48 > independent_scalar48.log
python independent_scalar.py 70 > independent_scalar70.log
python regressions.py > regressions.log
