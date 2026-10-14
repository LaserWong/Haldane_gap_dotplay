# Geometry-contracted large ground seeds

Updated 2026-10-10 13:54 America/New_York / 17:54 UTC.

This directory records a completed checkpoint of the large-seed calculation. The work changed no baseline scientific files and made no remote publication. Its historical authorization ended at 2026-10-13 20:00 America/New_York / 2026-10-14 00:00 UTC.

## Result

The exact one-block Krylov ground space now scales to 8×8 without physical-configuration enumeration. Its independent linear dimensions are **11,29,29** on **4×4,8×4,8×8**. The full Hilbert dimensions are 4^16,4^32,4^64. Each file retains one proposed ground state. The representation is not an MPS.

The method contracts three q4 matching tensors and fifteen q6 matching tensors per reached occupation set. One geometry calculation provides polynomial coupling dependence, supporting every rational g in the exported moment calculation. Its output includes exact B-basis moments M0 through M4 and the complete trial G/H/H² matrices. Physical leakage beyond the trial subspace is included.

At g=.03, the existing affine all-sector Temple threshold gives the following comparison.

| Rung lattice | q2 Temple width | New block1 Temple width | New residual squared |
|---|---:|---:|---:|
| 4×4 | .000351665 | 9.69152270434e-7 | 5.31536779901e-7 |
| 8×4 | .00220235 | 1.51499508555e-5 | 5.80717302568e-6 |
| 8×8 | .0217527 | .000332896372504 | 5.29130927402e-5 |

Exact trial files are supplied for g=.01,.02,.03,.04,.05 on all three sizes. At .04 on 8×8 and .05 on 8×4/8×8, the old affine second-level threshold is insufficient for Temple. These files deliberately have null lower endpoint and width but complete exact trial moments, Rayleigh quotient, and residual. The parallel complete-band calculation uses stronger number-sector comparisons and was integrating these data at this checkpoint. An old-threshold failure is not a statement about physical gaplessness.

## Checks and resource use

- Independent direct physical-spin action exactly reproduces the symbolic matching rules on all 76 q0/q2/q4/q6 matchings on 3×2, including TT signs, DD contractions and parallel edges.
- All 225 q6 matching Gram entries exactly equal 3 raised to the union-loop count, after removing factor 2^N.
- After an explicit basis transformation, every saved block1 G/H/H² entry agrees on 2×2,4×2,4×4 for g=.01,.02,.03.
- All 15 exported large-seed files pass exact rational replay of moments, trial norms, energies, residuals and applicable Temple endpoints.
- The 8×8 contraction examines 635,376 q4 sets and 10,585,856 reachable q6 sets, rather than all 74,974,368 q6 sets. It stores 13,706,880 candidate 64-bit masks before deduplication.
- Initial 8×8 shared-load run: 17.34 seconds. Capped repeat: 5.46 seconds, 106.25 MiB geometry-process peak RSS. The Python driver peak was about 76.5 MiB. The repeat imposed a 1.5 GiB process address-space cap and one CPU/BLAS thread and reproduced every F/S/V/W integer entry. Timing is load-dependent, not a hardware-independent benchmark.

These are internal exact-arithmetic and independent-formulation checks. The package remains a candidate pending independent-worker audit and the separate complete trace/transfer proof. A small residual alone does not establish spectral completeness.

## Files

- `PROOF.md`: complete matching algebra, block formulas, integer bounds, and scope
- `contract_geometry.cpp`: streamed integer geometry contractions F,S,V,W
- `large_seed_moments.py`: reusable exact matrix and certificate API
- `verify_moments.py`, `verification.json`: direct physical-spin and saved-matrix tests
- `replay_certificates.py`, `exact_replay.json`: exact arithmetic replay of all 15 candidates
- `geometry_*.txt/json`: replayable geometry input and exact contracted output
- `block1_*.json`: matrices, moments, rational coefficient vectors and available intervals
- `benchmark_8x4.log`, `benchmark_8x8.log`, `capped_repeat.log`: measured runs
- `MANIFEST_SHA256.json`: stable package checksums, excluding itself and bytecode

## Reproduce

Run from this directory. Commands affect only local generated files. No remote state changes.

    c++ -O3 -std=c++17 -Wall -Wextra contract_geometry.cpp -o contract_geometry
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python verify_moments.py
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python large_seed_moments.py --nx 8 --ny 8 --g 3/100
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python replay_certificates.py

Geometry caches are reused. To explicitly rebuild and compare a geometry, call `geometry(nx,ny,force=True)` and compare its F/S/V/W fields against the previous values. The C++ process is bounded by a ten-minute subprocess timeout in the driver. Inputs are restricted to N≤64, at most 20 pair orbits, degree four and edge multiplicity at most two. Python certificate arithmetic uses unbounded integers.

## Remaining research

1. Complete the independent audit of these geometry moments and the larger complete-low-band integration.
2. Re-evaluate the combined trace/transfer bottleneck using the sharper ground intervals.
3. Only if ground width remains limiting, extend the q4 trial basis beyond the single block. Estimate orbit count, q6 contractions and memory first. This is a prospective extension, not an implemented result here.
