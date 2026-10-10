# Independent spin-2 heat-kernel audit

Updated: 2026-10-10 13:59 EDT (America/New_York) / 17:59 UTC.

## Result

**PASS for the frozen mathematical error argument and the three named kernels.**
The forward Chebyshev recurrence, parity compression, signed64 split products,
and column blocking preserve the claimed rigor. No blocking defect was found.
The old sub-1/Q polynomial bound omitted quantization; the corrected strict
bound **75/Q**, Q=2^56, is independently verified.

The physical model is the unit-coupling, periodic, isotropic spin-2 Heisenberg
chain, with seam twists I, P, C (1, -1, exp(2 pi i/3)), beta=8, and thermal
shift a=5951/1250. The audited executable range is 3 <= L <= 10.
This is an algorithm/error certification and small-volume validation. It is
**not a completed L9/L10 heat trace, a uniform spin-2 gap certificate, or a
rigorous runtime guarantee**.

### Independently completed checks

- Regenerated both Chebyshev and Horner coefficient files and every stored
  rational error term from exact integers. Both files match byte-for-byte.
- Constructed a separate physical ring matrix using raising moves and their
  Hermitian adjoints, then used independent Python-bigint ring arithmetic.
- Checked every symmetry representative in every nonpositive magnetization
  sector at L3 and L4, for all three twists: **255 columns, 48 sector/twist
  combinations, and 50,772 four-component integer coordinates**.
- Freshly compiled uncompressed, compressed, and final fast sources using
  C++20 with UBSan and no sanitizer recovery. Every coordinate matched at
  block sizes 1, 2, 4, 8, including short batches and nonzero starting indices.
- Reconstructed all six L3/L4 complete trace enclosures. The three L4 integer
  totals and exact rational intervals reproduce the producer's outputs.
- Independently reconstructed all 27 archived L4 GMP input matrices. The
  archived exact rational outputs, with their analytic tails, lie strictly
  inside the new L4 intervals. The costly archived GMP jobs were not rerun.
- Rechecked the open-eight witness by an independent row-oriented integer
  application: 38,165 states, 358,904 offdiagonal entries, minimum integer
  margin 839778326.
- Recomputed exact sector dimensions, Burnside orbit counts, and edge counts
  at L3, L4, L8, L9, L10, plus both large-size error budgets.
- Proved uniform signed64/signed128 range bounds stronger than checking only
  the small test cases; see [AUDIT_PROOF.md](AUDIT_PROOF.md).

### Small complete traces

The following are decimal displays only. The exact rational endpoints in
`results/independent_exact_audit.json` are the certificates.

| L | Twist | Z lower display | Z upper display |
|---|---|---:|---:|
| 4 | I | 2112.032181155256 | 2112.0321811721797 |
| 4 | P | 0.014893392655195513 | 0.014893392700136307 |
| 4 | C | 0.16901418568064375 | 0.16901418583203665 |

The full Hilbert dimensions are 5^3=125 and 5^4=625. The largest test
magnetization block is 85. No dense eigensolver was used in this audit.
Orbit representatives are computational trace columns, not a variational
trial space or an MPS bond dimension.

## Large-size limits and launch prerequisites

At L9/L10, all-sector Frobenius error numerators are respectively 340727888
and 1658650919. Thermal norm errors are bounded by approximately
2.88536e-7 and 2.21786e-6. The associated approximate trace-error bounds
5.77072e-6 and 4.43571e-5 **are conditional on Z <= 100**. This audit has
not verified that condition. Direct rational norm enclosures remain valid
without it after all required columns are completed.

Exact work counts are 55,199 and 247,113 representatives per twist at L9
and L10, with 90,555,397,975 and 2,119,000,652,898 representative-weighted
stored-edge visits per recurrence application. Runtime projections made by
scaling single/batched M0 benchmarks are estimates: they omit a proof of
cross-sector timing behavior and do not certify completion by a deadline.
The frozen cost budget describes the older uncompressed timing measurements;
later compressed timing records must retain their own source/executable hashes.

Before a long campaign, add an atomic, identity-bound per-chunk resume layer
for these kernels and verify missing-sector tail inputs for the same L, beta,
a, and twist. The current one-line-per-column stdout and atomic whole-benchmark
record are sufficient for bounded benchmarks, not a complete resumable campaign.
No large trace or remote update was performed by this audit.

## Frozen inputs and reproducibility

The producer confirmed `snapshot_initial` as the audit target. Its initial
47-file manifest has SHA256
`3f14e5ae2fcda113f8a62dd9721451efd1d981a502a89440c032291a39a04d75`.
The final fast kernel was separately confirmed by the producer to have the
same hash already present in this snapshot.

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

The exact-column check took about 93 seconds; the bounds check took about one
second in this environment. Tests and compiles were sequential and capped at
1 GiB address space. `audit_bounds.py` reads the preserved original open-eight
witness from the repository. All writes made by this review are contained in
this directory. The extracted repository has no `.git` metadata; the parent
status records source commit `6be889a30f642bde77fb89af75b3a7379615bed1`.
