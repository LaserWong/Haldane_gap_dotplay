# Ordered periodic Ising: exact ground gap versus low-band separation

## Result and scope

For every integer L >= 2, use Pauli matrices and

    H_L = -sum_i Z_i Z_(i+1) - (1/2) sum_i X_i,
    Z_L = Z_0.

The sum has L positive-direction bonds, so L=2 contains two copies of
Z_0 Z_1. Ordered eigenvalues E_0 <= E_1 <= E_2 include multiplicity.
The following are analytic conclusions, not extrapolations from numerical ED:

- The exact finite-volume ground multiplicity is g_L=1.
- Delta_L = E_1-E_0 is positive for every finite L and tends to zero
  exponentially fast (an explicit exponential upper bound is below).
  Consequently inf_{L>=2} Delta_L = 0.
- The bottom two states form a band of width Delta_L. Its complementary
  separation Gamma_L = E_2-E_1 tends to 2. Also E_2-E_0 tends to 2.
  These are separations above a low-energy band, not the finite-volume
  excitation gap above the exact ground space.

No claim about an infinite-volume representation's spectral gap or a
symmetry-breaking boundary-condition limit is needed here. This note is
local research, not a new registered CLI route or interval certificate.

## 1. Unique ground state without a supplied ground rank

In the computational Z basis all off-diagonal entries of H_L are either
-1/2 (one spin flip) or zero. Single-spin flips connect the entire Boolean
hypercube. Choose c large enough that A=cI-H_L is entrywise nonnegative.
A is irreducible. The Perron–Frobenius theorem gives a simple largest
eigenvalue with strictly positive eigenvector; this is the unique ground
vector psi of H_L. Thus g_L=1 exactly, without diagonalization.

The global spin flip P=product_i X_i commutes with H_L and permutes the
computational basis. Uniqueness makes psi a P eigenvector; strict positivity
forces its eigenvalue to be +1. In particular the lowest P=-1 energy is
strictly above E_0, however small its difference may be.

## 2. Physical parity sectors and the first three levels

The same Jordan–Wigner/Bogoliubov mode decomposition used in
`gapflow/quantum_ising.py` gives

    epsilon(k) = 2 sqrt(1 + 1/4 - cos(k))
               = 2 sqrt(1/4 + 2 sin(k/2)^2),
    K_NS = {2 pi (m+1/2)/L : m=0,...,L-1},
    K_R  = {2 pi m/L : m=0,...,L-1},
    V_NS = -(1/2) sum_{k in K_NS} epsilon(k),
    V_R  = -(1/2) sum_{k in K_R} epsilon(k).

For clarity, rotate spin axes so the field is the fermion number axis.
The Jordan–Wigner boundary sign is antiperiodic for P=+1 (NS), periodic
for P=-1 (R). Paired k,-k Bogoliubov transformations preserve parity.
The unpaired R zero-momentum mode changes its vacuum occupation when
h crosses J. For h<J the R Bogoliubov vacuum has physical parity -1;
the NS vacuum has physical parity +1. Both physical sectors therefore
retain *even quasiparticle occupation*. This is exactly the `h < J`
branch selecting `even` for R in the existing positive-parity recurrence.
The fact that physical R parity is odd does not impose odd quasiparticle
number in this ordered regime.

Every physical level is V_s plus a sum of an even number of distinct
positive epsilon modes in its sector. The vacua are sector minima.
Section 1 identifies E_0=V_NS. Let delta=V_R-V_NS>0.

There is also a convenient non-numerical bound delta<=1: Z_i psi is a
normalized odd-parity trial state and

    <Z_i psi,H_L Z_i psi>-E_0 = <psi,X_i psi> <= 1.

Every non-vacuum even-occupation state has at least two quasiparticles,
each with epsilon>=1. Thus V_R<=V_NS+1 lies strictly below the first
NS excitation (which costs at least 2); the two vacua are exactly the
bottom two states for every L>=2.

The least pair costs are

    a_NS(L) = 2 epsilon(pi/L),
    a_R(L) = epsilon(0) + epsilon(2 pi/L).

NS has the distinct modes +/-pi/L. R's two cheapest distinct modes
are zero and +/-2pi/L (at L=2 the latter is just pi). Therefore, exactly,

    E_1 = V_R,
    E_2 = min{V_NS+a_NS(L), V_R+a_R(L)},
    Delta_L = delta,
    Gamma_L = min{a_NS(L)-delta, a_R(L)}.

This formula also covers odd L; no even-size restriction is imposed.
Since delta<=1 and both pair costs>=2, Gamma_L>=1 for every L>=2.
As L grows both pair costs tend to 2, so delta->0 implies Gamma_L->2.
For general 0<h<J the pair-cost limit is 4(J-h); the elementary
all-size bound delta<=2h only proves the same two-vacuum ordering when
it is smaller than the pair threshold. Analytic small splitting proves
that ordering for sufficiently large L throughout the ordered regime.

## 3. Exact exponential bound by analytic Fourier coefficients

This proof supplies the asymptotic assertion independently of floating data.
Put q=1/2 and, on the annulus q<|z|<1/q, define

    f(z) = 2 (1-q z)^(1/2) (1-q/z)^(1/2)
         = sum_{n in Z} c_n z^n.

Each square root is its convergent binomial-series branch, so the function
is single valued and analytic throughout this annulus; f(e^(ik))=epsilon(k).
For any 1<rho<2, the two contour bounds give

    |c_n| <= M_rho rho^(-|n|),
    M_rho = 2 sqrt((1+q rho)(1+q/rho)).

Discrete sums over R and NS momenta retain only Fourier indices divisible
by L, with factors 1 and (-1)^j respectively. Hence

    delta = -L sum_{j odd, j in Z} c_(jL),
    0 < delta <= 2 L M_rho rho^(-L)/(1-rho^(-2L)).

Taking rho=3/2, M_rho<4, gives the simple explicit bound

    0 < Delta_L < 8 L (2/3)^L / (1-(2/3)^(2L)).

It tends to zero exponentially; no fitted slope or unproved asymptotic
prefactor is used. The inequality is deliberately loose at small L.
Combined with the exact first-three-level formulas, it proves both limits.

## 4. Contrast with the zero-field endpoint

At h=0 the two aligned configurations are exactly degenerate ground states,
g_L=2, and the first excited configurations have two domain walls costing
4J, including the doubled-bond L=2 convention. For every h>0 the connected
spin-flip matrix instead has g_L=1. For 0<h<J its parity splitting tends to
zero with volume. Thus the definition E_(g_L)-E_0 changes which index it
uses at h=0: exact ground rank and near-degenerate band rank cannot be
interchanged. At fixed L the nonzero splitting tends to zero as h->0+,
whereas the gap above the exact h=0 ground space is 4J.

## 5. Independent numerical audit and resource scope

Reproduce with installed NumPy/SciPy only:

    OPENBLAS_NUM_THREADS=1 python benchmarks/run_ordered_ising_low_band.py

The script builds an independent Z-basis matrix-vector action (no production
Hamiltonian builder), requests only four lowest eigenpairs using `eigsh`,
and checks their residuals and global-spin-flip expectation values.
A separate mode calculation retains four minimum even/odd subset costs
per recurrence step; it does not enumerate a many-body spectrum.
It compares the four predicted levels to the independent Ritz values.
All integers L=4,...,12 are included, full working dimensions 16 through
4096. Incremental memory is admitted conservatively before basis allocation;
the admitted ceiling is 256 MiB and 20 seconds. Runtime and process peak
RSS, solver residuals, and discrepancies are saved in
`benchmarks/ordered_ising_low_band.json`. These caps are checked by the
bounded script, not installed as operating-system hard limits.

Representative floating values:

| L | E_1-E_0 | E_2-E_1 |
|---|---:|---:|
| 4 | 0.0354904326399 | 2.91176108378 |
| 8 | 0.00145584750079 | 2.28282248051 |
| 12 | 0.0000724687869162 | 2.13187189713 |

Ritz values, mode evaluations, and small residuals are floating evidence,
not exact lower bounds or verified spectral-count certificates. The exact
ground rank, positivity, exponential upper bound, and limiting separation
come from Sections 1–3, not this table.

## 6. Implication for model-input workflows with unknown g

A model-only input need not ask the user to supply ground rank. It must,
however, keep its requested spectral target explicit:

1. Exact-ground-space gap: infer g by valid analytic or exact spectral
   evidence, then bound E_g-E_0. For this family g=1 and no positive
   volume-uniform bound exists.
2. Separation above an r-state low-energy band: certify its count r,
   width E_(r-1)-E_0, and complement separation E_r-E_(r-1).
   Here r=2 has exponentially shrinking width and a positive uniform
   separation (the simple bound here is 1), tending to 2.

A rank-two numerical cluster cannot be renamed a twofold exact ground
space. A thermal purity near 1/2 over an intermediate temperature window
is compatible with this unique ground and small splitting; cooling each
fixed finite matrix eventually yields purity 1. Failure of a rank-one
thermal bootstrap is not evidence against the positive two-state-band
separation, and success of a band certificate is not a rank-one gap proof.

See `UNKNOWN_MULTIPLICITY_BOOTSTRAP.md` for general counted-cluster logic
and `DEGENERATE_PURITY.md` for the distinct thermal targets. The current
paramagnetic `quantum_ising_chain` production route requires h>J; this
ordered example does not relax or modify that route's proof guard.
