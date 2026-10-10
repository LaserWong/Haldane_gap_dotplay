Updated: 2026-10-10 14:02 EDT / 18:02 UTC

# Spin-2 heat-trace audit and bounded optimization

## Result and allocation recommendation

The streamed Chebyshev error proof and bounded implementation tests have passed
[independent review](../spin2_heat_review/README.md), with no blocking findings. No complete
L9/L10 trace, accepted spin-2 bootstrap seed, or uniform spin-2 gap is claimed.
Do **not** launch a full trace campaign for the current archived startup route:
its optimistic scalar screen still fails, and the L10 critical path exceeds the
remaining two-core research window even after the measured speedups.

### Validated implementation progress

- Exact positive Chebyshev coefficients regenerate bitwise; implemented degree
  136 versus degree 400 for the comparable fixed-point Taylor/Horner method.
- Correct total polynomial error is <75/Q, Q=2^56. The older <1/Q metadata
  covered normalization/truncation alone and omitted coefficient quantization.
- The error theorem now includes every recurrence floor, coefficient-product
  floor, symmetry multiplicity, Frobenius bound and finite exponential bound.
- All conjugate embeddings are controlled by an explicit local parity gauge,
  closing the quadratic-field integer-overflow argument.
- A parity invariant halves the active coordinate count; exact split matvecs
  avoid signed128 sparse products, and four-column batches reuse graph reads.
- 36 independent Python-bigint reference columns pass bitwise. The compressed
  and final fast kernels pass all 36 small block/twist/batch configurations,
  including short final batches, under UBSan. Large benchmark first columns
  also match the uncompressed result exactly.
- Complete L4 I/P/C streamed trace intervals contain freshly reconstructed
  independent GMP intervals. All three GMP numerators and denominators exactly
  reproduce the historical archive. No eigensolver was used in this full-trace
  check. A separate diagnostic eigensolver was limited to blocks of size <=85.
- The open-eight lower-bound witness was freshly rechecked in 38,165 exact
  integer inequalities. Original paused sources and results retain their hashes.

### Measured speed and memory

All timings are bounded local benchmarks, not runtime guarantees. Both sides of
the L9 speedup comparison use -O3 -march=native on this same executor.

| L, M | Kernel | I seconds/column | C seconds/column |
| --- | --- | ---: | ---: |
| 9, 0 | uncompressed Chebyshev, native build | 4.624 | 8.683 |
| 9, 0 | compressed/split, four columns | 0.570 | 2.852 |
| 10, 0 | compressed/split, four columns | 3.890 | 13.749 |
| 10, -4 | compressed/split, four columns | 2.404 | 6.943 |

Matched L9 speedups are **8.1x for I and 3.0x for C**. A generic, non-native
uncompressed build was slower still, but that compiler penalty is excluded from
these headline factors. The tested eight-column batches regressed; four columns
are selected. Peak measured RSS for the selected L10 run was 776.3 MiB. Each
benchmark child was limited to one numerical thread, 2 GiB address space and
600 seconds. All completed records include source/executable/coefficient hashes.

### Exact work counts and projected full costs

Burnside counting gives 55,199 representatives at L9 and 247,113 at L10, summed
over all M<=0, with the positive-M partners included by multiplicity. The full
Hilbert dimensions are 1,953,125 and 9,765,625; the largest M blocks are 180,325
and 856,945. These are not trial-space or MPS bond dimensions.

Projection sums representative_count(M)*stored_edges(M) across **every sector**.
It does not multiply a worst-case M0 column by the total column count.

| Complete target | Estimated core-hours |
| --- | ---: |
| L9, I/P/C | 42.8 |
| L10, I/P/C | 846.7–1034.0 |
| L10, I/P only, retaining M=0,...,4 | 293.3–316.3 |

The L10 range uses the observed M0 and M=-4 cost-per-edge rates; it is not a
statistical confidence interval. P is assigned the same operation-rate model
as I. Large chunks are assumed to reuse a built CSR graph; setup and checkpoint
I/O are additional costs. Tail omission requires a compatible certified bound,
not just deleting those sectors. Even the last row exceeds the remaining
window ending 2026-10-14 00:00 UTC on two cores. No full run was launched.

### Mathematical feasibility screen

The original incomplete order-10 moments already failed its tested bootstrap
family. Updating to the later D124-certified energy shift a=4.76121 leaves the
optimistic beta8 support caps at J=1.111114 and N=1.085112. The nontrivial-sector
mass upper bound alone is about 105,876 at N=128, where the atom-exclusion step
requires the whole bound below 1. All tested beta=6,8,10,12,16,20,24,32 and
N=128,256,512,1024 fail, including the uncertified D180 shift sensitivity test.

These are scalar diagnostics based on **uncertified** L9/L10 Ritz moments. They
rule out allocating this expensive run for the presently proposed startup,
not the physical gap or every possible filter. A successful alternative scalar
proposal and an explicit trace-error budget should precede any long campaign.
See [seed feasibility](seed_feasibility/README.md).

The independent auditor additionally reconstructed 255 complete L3/L4
representative columns across all sectors, all batch sizes and nonzero starts,
and verified the archived GMP matrices and exact work/error bounds. The proof
files retain their reviewed author-snapshot text; the linked independent review
provides the later sign-off.

## Evidence and audit entry points

- [Independent audit and frozen-source manifest](../spin2_heat_review/README.md)
- [Mathematical next steps and exact seed obstruction](NEXT_STEPS.md)
- [Complete error and range proof](PROOF.md)
- [Compressed/split/blocking proof](COMPRESSED_PROOF.md)
- [Exact coefficients](results/coefficient_audit.json)
- [Reference bigint tests](results/kernel_validation.json)
- [Compressed tests](results/compressed_validation.json)
- [Final fast-variant tests](results/variant_validation.json)
- [Small complete trace/GMP checks](results/full_L4_validation.json)
- [Exact sector work counts](results/exact_work_counts.json)
- [Initial error and cost budget](results/cost_error_budget.json)
- [Selected optimized cost model](results/optimized_cost_model.json)
- [Original-input integrity and environment](results/input_integrity.json)
- [Scalar screen](seed_feasibility/seed_screen.json)

The exact operator/Frobenius error bound remains useful independently of the
negative scalar screen. At the present Q, the conservative shifted Frobenius
norm error is <=2.886e-7 for L9 and <=2.218e-6 for L10. Actual trace interval
widths also depend on the computed trace magnitude. No unchosen future seed
accuracy requirement is assumed to have been met.

## Reproduce without a large run

From this directory:

    sh build.sh
    python prepare_coefficients.py
    python verify_cluster.py
    python count_work.py
    python validate_kernel.py
    python validate_compressed.py
    python validate_variants.py
    python validate_full_L4.py
    python report_budget.py
    python summarize_optimized_cost.py
    python seed_feasibility/screen_seed.py

The complete L4 reference check can reuse already completed original GMP logs;
its initial recorded run was fresh. `build.sh` requires g++ and GMP. Python
validation needs NumPy; all accepted error arithmetic uses Python integers and
Fractions. Source paths outside this directory are limited to the unchanged
baseline coefficient/prototype and the archived open-eight witness, all in the
parent repository. The selected legacy H4 program/inputs and scalar-screen
inputs were copied with provenance, so the larger sibling archive is no longer
needed for reproducing those checks.

A bounded L10 optimized sample can be rerun with:

    python benchmark.py --L 10 --compressed --fast --block 4 --count 4 --algorithms chebyshev

This is eight total columns, four per twist, not a complete trace. The benchmark
wrapper preserves completed hashed records and rejects mismatching cache
identities. These records are benchmark checkpoints; a long production driver
with persisted CSR graph and atomic per-chunk acceptance has not been deployed.

## Next useful steps

1. Independent review is complete with no blocking findings; preserve the reviewed
   source hashes and the original large-trace/conditional-budget scope limits.
2. Seek a genuinely stronger scalar/moment startup that succeeds with optimistic
   data before committing days of exact trace work.
3. If such a proposal appears, choose beta, required twists/orders and rational
   accuracy first; raise precision only as justified by that budget.
4. For a later production kernel, release the original CSR graph after
   compression, mark whole symmetry orbits visited during representative
   enumeration, and retain graphs across checkpoint chunks. These save setup
   time/memory but do not remove the fundamental all-column work estimate.
5. A signed128 final accumulator could postpone its 137 coefficient floors to
   one final floor and tighten the error bound. This is a future option, not an
   implemented or benchmarked result.

No background computation is required to hold this checkpoint. All project-wide
GitHub updates and any new resource allocation belong to the parent task.
