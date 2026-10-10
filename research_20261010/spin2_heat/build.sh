#!/bin/sh
set -eu
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
CXX=${CXX:-g++}
$CXX -std=c++17 -O3 chebyshev_columns.cpp -lgmpxx -lgmp -o heat_columns
$CXX -std=c++17 -O3 -march=native chebyshev_columns.cpp -lgmpxx -lgmp -o heat_columns_native
$CXX -std=c++17 -O1 -g -fsanitize=undefined -fno-sanitize-recover=all chebyshev_columns.cpp -lgmpxx -lgmp -o heat_columns_ubsan
for variant in compressed phase fast profile; do
  case "$variant" in compressed) src=compressed_columns.cpp;; *) src=compressed_${variant}.cpp;; esac
  $CXX -std=c++20 -O3 -march=native "$src" -lgmpxx -lgmp -o "heat_$variant"
done
$CXX -std=c++20 -O1 -g -fsanitize=undefined -fno-sanitize-recover=all compressed_columns.cpp -lgmpxx -lgmp -o heat_compressed_ubsan
$CXX -std=c++20 -O1 -g -fsanitize=undefined -fno-sanitize-recover=all compressed_fast.cpp -lgmpxx -lgmp -o heat_fast_ubsan
