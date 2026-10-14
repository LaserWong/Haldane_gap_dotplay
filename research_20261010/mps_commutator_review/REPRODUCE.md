# Reproducing the commutator calculation

Use a new scratch copy preserving the research directory layout. Do not rerun writers in a sealed tree. GMP C++ development headers, g++17, Python3 and NumPy are required. All commands use CPU1 and one thread.

Begin with the small-system checks.

    taskset -c 1 python independent_tiny.py
    taskset -c 1 python independent_cells.py
    taskset -c 1 python independent_fsum.py

The cell reconstruction takes approximately 68 CPU seconds. To rebuild the distinct contraction engine, run

    taskset -c 1 g++ -O3 -std=c++17 independent_contract.cpp -lgmpxx -lgmp -o independent_contract

Full n24 replay is a separately budgeted computation, not part of the cheap verification. The archived driver records immutable source/binary/cell hashes and refuses unknown prior accounting. An existing complete checkpoint is not recomputed. For a genuinely new reproduction, create a separate run directory, keep the original checkpoint intact elsewhere, and explicitly initialize a fresh checkpoint/input manifest under the same 2400-CPU-second/700-MiB cap. Do not erase or mutate an interrupted original checkpoint. The binary accepts cells.txt, n, and a list of mix:r / jj:r queries. All 24 mixed and 13 JJ cases are required. Its exact output must match independent_n24.out.

Once exact n24 replay has completed, run

    taskset -c 1 python independent_assembly.py
    taskset -c 1 python independent_scalar.py
    taskset -c 1 python regressions.py

The arithmetic checks compare all 74 integers, Gram/H forms, positive determinant, exact orthogonal rational directions, spin multiplicities, and every scalar box. They also validate every producer freeze and the three earlier independent-review manifests. Regeneration changes measured resource fields, so do not compare whole timing-bearing JSON files byte-for-byte. Compare exact scientific fields and all integer outputs. Immutable archived hashes identify the original run.
