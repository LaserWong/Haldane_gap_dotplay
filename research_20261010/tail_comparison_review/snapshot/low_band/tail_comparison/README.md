# Same-input comparison of whole-spectrum tails and bootstrap order

2026-10-10 14:34 America/New_York / 18:34 UTC.

All physical trial moments, the three tail theorems, the permutation transport,
and the finite-window interpolation used here have independent upstream audits.
The recombination records in this directory remain candidates until their own
independent exact replay is complete. No physical vector was regenerated.

The model is the ordinary periodic spin-1/2 square bilayer, unit rung coupling
and equal straight in-layer coupling g. The maximum seed is 8x8 rungs, with full
Hilbert dimension 4^64, a 29-dimensional ground trial and a complete retained
low band of dimension 193. This comparison does not claim an optimal physical
gap, optimal coupling, or minimum seed among arbitrary geometries.

## Best all-integer candidate from the same bounded temperature grid

All listed best choices use a time,x,y cycle followed by exact transport to the
canonical x,y,time staircase; the code labels the original order txy. Time is
never relabeled as a spatial direction.

| g | original number tail | bosonic Jacobi tail | quadratic boson reference |
|---|---:|---:|---:|
| .03 | .317881464188 | .317999803724 | .318085460990 |
| .04 | .234445519760 | .234841332964 | .235117964607 |
| .05 | .170554842579 | .171296530205 | .171822115684 |
| .06 | .099555868340 | .101960334497 | .103487228301 |

Every displayed candidate includes all integer square sides L>=2. Canonical
finite-window bounds fill the pre-acceptance dyadic windows. The fixed .06
number-compression comparisons cover sizes L=2,...,7 for every 0<=g<=.06: smaller
g has a larger preserving-block lower bound and a smaller pair-creation norm
upper bound. This is a quadratic-form comparison with the same scalar Jacobi
matrix, not an assumption that the physical gap is monotone in g.

The major gain compared with the previously published canonical-only .03–.05
records comes from applying the independently proved order transport. The table
separates that gain from the smaller like-for-like tail improvement.

## Spectral counting conventions

- `original/` uses the previously audited occupancy/Jacobi physical number bins.
- `jacobi/` replaces their off-block estimates by the minimum of occupancy and
  independently reviewed bosonic creation-norm bounds. Multiplicities remain
  binomial(N,q)*3^q.
- `quadratic/` uses the complete stable oscillator reference separately, with
  multiplicities binomial(3N+q-1,q). Its finite q<=N sum is the independently
  proved overcount of the ordered finite physical spectrum.

The code does not take pointwise maxima of endpoints with different ordered
index breakpoints. All three methods agree on the first retained count 1+3N;
that counted cutoff is used in the sector-Temple intervals for the same frozen
physical moments. New cutoff, lower interval, trace and bootstrap data are
saved separately for each variant.

## Exact arithmetic and provenance

Every patch rereads and exactly contracts its ground G/K/J matrices, and uses
exact Q(sqrt(2)) triplet Rayleigh/residual data. Source SHA-256 values are included
in every patch. The temperature grid beta=5,...,30 in steps of .05 proposes
candidates only. Every selected success is re-evaluated with directed dyadic
exponentials, rational square-root bounds, and exact canonical recursion and
finite-window gap acceptance.

Run from the repository root, with single-thread BLAS and no bytecode writes:

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/tail_comparison/integrate_tails.py --variant original
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/tail_comparison/integrate_tails.py --variant jacobi
    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/low_band/tail_comparison/integrate_tails.py --variant quadratic

These commands regenerate the local records. Preserve the frozen hashes when
replaying for audit or publication.
