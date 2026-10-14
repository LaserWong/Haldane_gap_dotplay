# Independent spin-2 heat-kernel audit

Updated: 2026-10-10 13:59 EDT (America/New_York) / 17:59 UTC.

## Audit result

**PASS for the frozen mathematical error argument and the three named kernels.**
The audit found no blocking defect in the forward Chebyshev recurrence, parity
compression, signed64 split products or column blocking. These operations
preserve the claimed rigor. The earlier sub-1/Q polynomial bound omitted
quantization. The corrected strict bound **75/Q**, Q=2^56, is independently
verified.

The audit concerns the unit-coupling periodic isotropic spin-2 Heisenberg
chain with seam twists I, P, C (1, -1, exp(2 pi i/3)), beta=8, and thermal
shift a=5951/1250. The audited executable range is 3 <= L <= 10.
It certifies the algorithm and error argument and validates small volumes.
It does **not provide a completed L9/L10 heat trace, a uniform spin-2 gap
certificate, or a rigorous runtime guarantee**.

### Independent checks completed

- Regenerated both Chebyshev and Horner coefficient files and every stored
  rational error term from exact integers. Both coefficient files match byte-for-byte.
- Constructed a separate physical ring matrix using raising moves and their
  Hermitian adjoints, and evaluated it with independent Python-bigint ring arithmetic.
- Checked every symmetry representative in every nonpositive magnetization
  sector at L3 and L4, for all three twists: **255 columns, 48 sector/twist
  combinations, and 50,772 four-component integer coordinates**.
- Compiled the uncompressed, compressed and final fast sources afresh using
  C++20 with UBSan and no sanitizer recovery. Every coordinate matched at
  block sizes 1, 2, 4, 8, including short batches and nonzero starting indices.
- Reconstructed all six L3/L4 complete trace enclosures. The three L4 integer
  totals and exact rational intervals agree with the producer's outputs.
- Independently reconstructed all 27 archived L4 GMP input matrices. Their
  archived exact rational outputs, including the analytic tails, lie strictly
  inside the new L4 intervals. The costly archived GMP jobs were not rerun.
- Rechecked the open-eight witness with an independent row-oriented integer
  application: 38,165 states, 358,904 off-diagonal entries, minimum integer
  margin 839778326.
- Recomputed exact sector dimensions, Burnside orbit counts, and edge counts
  at L3, L4, L8, L9, L10, plus both large-size error budgets.
- Proved uniform signed64/signed128 range bounds that extend beyond the small
  test cases. See [AUDIT_PROOF.md](AUDIT_PROOF.md).

### Small complete traces

The table displays decimal approximations. The certificates are the exact
rational endpoints in `results/independent_exact_audit.json`.

| L | Twist | Z lower display | Z upper display |
|---|---|---:|---:|
| 4 | I | 2112.032181155256 | 2112.0321811721797 |
| 4 | P | 0.014893392655195513 | 0.014893392700136307 |
| 4 | C | 0.16901418568064375 | 0.16901418583203665 |

The full Hilbert dimensions are 5^3=125 and 5^4=625. The largest tested
magnetization block has dimension 85. No dense eigensolver was used in this audit.
Orbit representatives are computational trace columns, not a variational
trial space or an MPS bond dimension.

## Large-size limits and launch prerequisites

At L9/L10, the all-sector Frobenius error numerators are respectively 340727888
and 1658650919. The thermal norm-error bounds are approximately
2.88536e-7 and 2.21786e-6. The corresponding approximate trace-error bounds
5.77072e-6 and 4.43571e-5 **require Z <= 100**, which this audit has not verified.
Direct rational norm enclosures do not require this condition, but they require
completion of all necessary columns.

Exact work counts are 55,199 and 247,113 representatives per twist at L9
and L10, with 90,555,397,975 and 2,119,000,652,898 representative-weighted
stored-edge visits per recurrence application. Runtime projections obtained by
scaling single/batched M0 benchmarks remain estimates. They do not establish
cross-sector timing behavior or guarantee completion by a deadline.
The frozen cost budget describes the older uncompressed timing measurements.
Later compressed timing records must retain their own source/executable hashes.

A long campaign first requires an atomic, identity-bound per-chunk resume
layer and verified missing-sector tail inputs for the same L, beta, a and twist.
The current one-line-per-column stdout and atomic whole-benchmark record
suffice for bounded benchmarks. They do not support a complete resumable campaign.
No large trace or remote update was performed by this audit.

## Frozen inputs and reproducibility

The producer identified `snapshot_initial` as the audit target. Its initial
47-file manifest has SHA256
`3f14e5ae2fcda113f8a62dd9721451efd1d981a502a89440c032291a39a04d75`.
The producer separately confirmed that the final fast kernel has the hash
already recorded in this snapshot.

| Source | SHA256 |
|---|---|
| chebyshev_columns.cpp | e7a47eb0bb8f32d9c1054e09a9db95ba911fa02ce13526d9bdba6eae79ebfc78 |
| compressed_columns.cpp | 6f8fe1cfc2430b1b924214fe14861e50a3465e5910d8e9f583e3640a619a693b |
| compressed_fast.cpp | a6ed33529dd576913c682e3847a2bb9ea147c42b4a1ca4a8d3d4002926566439 |
| coefficients_chebyshev_Q56.txt | 67eed20f1e6d573fb203ef41e87eb4413bfcb9a5810cc5b43e1b971b6edaf618 |
| coefficients_horner_Q56.txt | d3a21ed8bbd8805bbece040ec67151cbee8e65d838ba3632c9eaaff7221e4c54 |

From this directory, compile sequentially:

```sh
for source in chebyshev_columns compressed_columns compressed_fast; do
  g++ -std=c++20 -O1 -g0 -fsanitize=undefined -fno-sanitize-recover=all \
    snapshot_initial/$source.cpp -lgmpxx -lgmp -o bin/$source
done
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python audit_exact.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python audit_bounds.py
```

The exact-column check took about 93 seconds, and the bounds check took about
one second in this environment. Tests and compilations ran sequentially under
a 1 GiB address-space cap. `audit_bounds.py` reads the preserved original open-eight
witness from the repository. All review writes are contained in this directory. The extracted repository
has no `.git` metadata. The parent status records source commit `6be889a30f642bde77fb89af75b3a7379615bed1`.
