# Spin-2 higher-input campaign: certified magnetic-sector tails

**No uniform gap and no new complete ninth/tenth spatial moment are proved.**

New completed work provides substantially sharper, independently checkable bounds
on the omitted high-magnetization sectors of a ten-site spin-2 Heisenberg ring.
These bounds hold for every z-axis seam twist. The unresolved issue is eigenvalue
counting inside the low-magnetization sectors; a small Ritz residual does not fix it.

## Exact finite certificates

We computed positive integer test vectors for every magnetization sector of open
spin-2 chains of lengths 4, 6, and 8: 39 vectors and 223,438 component inequalities.
`verify_cluster_and_tail.py` regenerated all rational Hamiltonian entries and
checked every saved inequality using Python integers. Exponential upper bounds in
the accepted tail certificates are rational Taylor bounds, not floating estimates.

The floating eigensolver and positive power iteration only propose the vectors.
Their convergence, residuals, and spectral completeness are not proof premises.
The certificate can be verified without rerunning an eigensolver.

In the product basis r_j = 0,...,4, make the Marshall sign transformation and the
positive diagonal similarity D_r = sqrt(product_j binomial(4,r_j)). The resulting
Hamiltonian is real, with nonpositive off-diagonals and rational entries. Twice
this Hamiltonian is the integer matrix `A2`. A move (r,s)->(r+1,s-1) has entry
-(4-r)*s in A2; the reverse move has entry -r*(4-s). Diagonal entries are twice
sum_j (r_j-2)(r_(j+1)-2), over open-chain bonds.

For a strictly positive integer vector q, the component inequalities

    2 e_minus q_i <= (A2 q)_i <= 2 e_plus q_i

imply e_minus <= E_min <= e_plus. The lower bound follows directly from
Gershgorin after diagonal similarity by q, since all off-diagonal entries are
nonpositive. The upper bound follows from the Rayleigh quotient of D^-1 q.
Thus the eigenvalue bounds do not rely on assuming a Ritz vector is the ground
state. No assertion about higher-eigenvalue counts follows from this certificate.

## Transfer from an open cluster to a twisted periodic ring

Let e_l(m) be the certified ground lower bound in magnetization m for the open
l-site cluster K_l. For h>=0 define

    c_l(h) = min_(m=0,...,2l) [e_l(m) - h (l-1) m/l].

Spin inversion accounts for negative m. Each open cluster crossing the seam can
be gauged to the untwisted one without changing its magnetization. Summing all
translated cluster inequalities, with every bond counted l-1 times and every
site counted l times, gives the exact operator bound

    H_n(theta) - h M >= n c_l(h)/(l-1),   n >= l.

We maximize the resulting affine bounds in h (exactly over the finitely many
intersections) and over l=4,6,8. Results are `cluster_envelopes.json`.

For n=10 the selected lower bounds in sectors |M|=0,...,8 are approximately:

| Absolute magnetization | Energy lower bound |
|---:|---:|
| 0 | -48.734169554285714 |
| 1 | -48.48587701371429 |
| 2 | -47.97777747885714 |
| 3 | -47.096686646857144 |
| 4 | -45.75362266285714 |
| 5 | -43.88380612 |
| 6 | -41.36932157028571 |
| 7 | -38.42073132657143 |
| 8 | -35.05253243914286 |

The exact fractions in the JSON, not these rounded displays, are used below.

## Certified thermal tails at beta=8, a=5951/1250

For a sector lower bound B_m and exact sector dimension d_m,

    Tr_(|M|>=m0) exp[-8(H_10(theta)+10a)]
       <= sum_(m=m0,...,20) 2 d_m exp[-8(B_m+10a)].

The following are outward rational bounds:

| Omitted magnetic sectors | Certified trace upper bound |
|---|---:|
| Absolute M >= 5 | 1.0899e-7 |
| Absolute M >= 6 | 1.5338e-16 |
| Absolute M >= 7 | 6.3556e-27 |
| Absolute M >= 8 | 8.6887e-39 |

The earlier three-site bound certified only the |M|>=8 tail at 1.06081e-7.
The new result includes more sectors and/or yields a much smaller bound.
It does not certify states omitted within |M|<=4.

For x>=0 the implementation uses

    exp(-x) <= 1 / sum_(k=0,...,K) x^k/k!,

with exact Fraction arithmetic, followed by an outward rational rounding.

## Why this does not yet produce a tenth spatial moment

`low_sector_obstruction.json` quantifies the remaining problem. The same cluster
bounds applied to every state in M=0,...,4 give an unconditional trace upper bound
of 8.917983983589e9 at beta=8. This is far too weak for the intended spatial-moment
filter. Even after formally removing any 16 exact eigenstates per M sector, the
bound is still 8.91781658921e9. This latter diagnostic does NOT identify the old
Ritz lists as certified exact eigenstates or as complete below any cutoff.

A successful next certificate requires a count of ALL eigenvalues below suitable
cutoffs and outward enclosures of the retained eigenvalues, or a different direct
rigorous thermal trace method.

The exact M-sector dimensions for M=0,...,4 are respectively
856945, 837100, 780175, 693450, and 587400. Translation reduces the largest block
to 85735. At the identity twist, full SU(2) plus translation would reduce the
largest multiplicity block to 11403 (singlet blocks have dimensions 1946..2025),
but a coupled-spin Hamiltonian construction was not implemented. The P and C
seam twists break this SU(2) reduction. Sparse LDL/inertia certification was not
attempted blindly on 85k blocks: symbolic fill and validated factorization require
a separate controlled implementation. No sparse Cholesky/LDL package is installed
in this environment. Full dense 85k matrices alone would require about 59 GB.

`block_count.py` derives all SU(2) x translation dimensions using exact integer
word-period counting and checks the sum equals 5^10. These are dimensions only,
not completed diagonalizations.

## Reproduce

All scripts and certificate data are self-contained within this directory.
Dependencies: Python, NumPy, SciPy; threadpoolctl for the optional eigensolver stage.
No files from an external workspace path are required.

    python verify_cluster_and_tail.py
    python low_sector_obstruction.py
    python block_count.py

Optional regeneration of candidate vectors (delete or rename saved open*_m*.json
first, because generation caches them):

    python cluster_bounds.py --lengths 4 6 8

The `.json` vector files are the concrete positive-integer witnesses. The accepted
component inequalities and thermal bounds do not depend on IEEE floating-point
rounding assumptions, beyond the accuracy of Python integer/Fraction operations.
