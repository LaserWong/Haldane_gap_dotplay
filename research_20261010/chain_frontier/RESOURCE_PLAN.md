# Frontier resource plan

Updated 2026-10-10 13:38 EDT / 17:38 UTC.

All numerical commands use one BLAS thread, no more than two concurrent CPU-bound commands in this lane, a 2 GiB address-space ceiling for sparse producers, and a 600-second wall-time timeout with a 590/600-second CPU limit. Outputs are isolated by assigning the existing producer modules' OUT variables; baseline sources are never changed.

- n=4, depth 4: archived N=8 count 43,294 trial states, 245,870 residual-support states, about 326.5 MiB historical RSS and 15.52 seconds. Expected safely below 2 GiB and one minute. Actual frontier runs used 318.6–368.8 MiB; shared-system runtime varied 8.7–57.3 seconds.
- n=6, depth 3: estimate from depth-three support growth below 0.5 GiB and two minutes. Actual N=12 count 14,863 trial states, 187,930 reached states, 199.7 MiB process RSS and 8.28 seconds. Whole-space isolation rejected; no depth increase attempted for that seed because the second-bin threshold is substantially below the Ritz pivot.
- n=4, depth 5 at g=0.1615: the exact depth-four reached support supplies the next trial count, 245,870. The sparse assembly is expected to have roughly 7–10 million entries; Python assembly lists, reached-state dictionaries and sparse copies may approach 1.3–1.8 GiB. Expected runtime one to three minutes, with the 2 GiB address-space and ten-minute caps enforced. A MemoryError or timeout is an accepted resource boundary and will be reported; do not retry without a revised streaming implementation. This experiment tests whether the near-threshold depth-four rejection is residual-limited, because the optimistic all-beta envelope at this coupling remains inconclusive.

No full Hilbert-space matrix or diagonalization is built. For N=8, full dimension is 43,046,721; for N=12 it is 282,429,536,481. Trial dimension is a linear coordinate-support count, not an MPS bond dimension, and only one vector is retained.

## Completed depth-five measurement

The N=8 depth-five run completed in101.276854841seconds with peak RSS1,706,108KiB (1,666.12MiB), below the2GiB address-space ceiling. Actual reached support was939,326. The resulting interval width was2.37048574793e-7. No higher-depth or larger-seed run is planned in this pass: the exact all-beta envelope now excludes the specified ground-only recipe atg=0.1615, so more ground-state digits would not remove that obstruction.
