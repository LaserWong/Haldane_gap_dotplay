# Continuous ordinary spin-1/2 bilayer certificate through g = .09

Updated 2026-10-10 17:19 America/New_York (EDT) / 21:19 UTC.
Status: exact producer certificate, pending independent interval review.

## Result and scope

Seven adjoining closed rational intervals cover every real g in [17/200,9/100].
For the ordinary periodic square spin-1/2 bilayer, unit rung coupling, straight
intralayer coupling g, zero crossed coupling, and the inherited positive-direction
periodic bond multiplicities, every integer square side L >= 2 has a unique
finite-volume ground state and gap at least

    2894183477/500000000000 = .005788366954.

The unchanged, independently reviewed [0,.085] certificate adjoins this range.
Its smaller uniform bound 486442811/250000000000 = .001945771244 consequently
holds on the union [0,.09], subject to independent review of this new extension.
This is a sufficient rigorous lower bound, not a physical critical coupling,
a gap estimate, a monotonicity statement, or interpolation of point certificates.
There is no claim about arbitrary aspect ratios or infinite-volume uniqueness.

## The only new interval ingredient: a fixed enlarged numerator

Use H'(g) = H(g) + 3N/4 = Q + gV, N = 64 rungs. The independently audited
third-moment geometry defines a coupling-independent basis W = (B,L,U), where
B contains the vacuum and pair-orbit vectors, L=A42 B, and U=A44 L+A64 L.
Its 43 columns are independent. L lies in q=4, while the two summands of U
lie in the mutually orthogonal q=4 and q=6 sectors. W does not depend on g;
its identification with span(B,H'B,H'^2 B) for g>0 does not change that fact.

Let n=14 and d=n+1. The exact Gram matrix is

    G = [[Gb,0,0], [0,F,S], [0,S^T,V+W]],

where the last W in this displayed block is the saved geometry's q=6 Gram,
not the basis matrix. To avoid ambiguity, denote that block W6 below. The
exact Q first moment is

    A0 = diag_blocks(Gb diag(0,2,...,2), 4F, 4V+6W6),

with off-diagonal L/U blocks 4S and 4S^T. All B/L and B/U blocks vanish.
This follows from orthogonality of Q eigenspaces, including the two pieces
of U. The exact g=.09 enlarged matrix gives

    A1 = (A(.09)-A0)/(.09),       A(g)=A0+g A1.

This is an operator-affinity identity, not a polynomial inferred from point
samples. The replay independently checks the entire exact A(.10) matrix from
the separate .10 producer construction and checks the constant Gram matrix.
The exported numerator_matrix_polynomial.json contains G,A0,A1 explicitly.

For each coupling interval [a,b], an ordinary 43D generalized eigenproblem at
z=(a+b)/2 only proposes a vector. Its coefficients are rounded to integers
and saved. For fixed c, exact arithmetic gives

    rho64(g) = (c^T A0 c + g c^T A1 c)/(c^T G c).

The norm is strictly positive, and rho64 is affine on the entire interval.
The thermal Jensen bound Z64'(beta,g) >= exp(-beta rho64(g)) supplies ONE
retained numerator contribution. The search dimension 43 is not a retained
state count, Hilbert dimension, MPS bond dimension, or full diagonalization.
No enlarged-state residual, H'^6 moment, q=8 support, or largest-patch spectral
tail is required. The physical 128-spin full Hilbert dimension remains 2^128.

## Smaller denominator traces, inherited without alteration

The 4x4 and 8x4 rung patches use the exact fixed basis G/H'/H'^2 polynomials
and the existing q=1,3 translated odd family. Their ground-search dimensions
are 11 and 29; odd trial dimensions are 48 and 96. Total available search
spaces have dimensions 59 and 125, while the actual trace retained-state
counts are 49 and 97. Their full Hilbert dimensions are 2^32 and 2^64.

The fixed-center construction and proof are those of interval_range_0085/
PROOF.md sections 3-6 and its independent interval_range_0085_review seal.
In brief, fixed integer ground witnesses have affine Rayleigh rho(g) and full
convex quadratic residual variance. The bosonic reference

    r_q(g) = (3N/8)(2g-1)+(3N/8+q)sqrt(1-4g)

is concave. Endpoint minima of r_q-rho and endpoint maxima of the variance
therefore give uniform ground identification and even-sector Temple widths.
The fixed-center odd-mode first moments are affine and complete variances
convex quadratics over Q(sqrt(2)); directed 160-bit rational enclosures and
endpoint extrema supply uniform odd Temple lower endpoints. Exact dimension
counting identifies precisely the ground plus 3N odd levels below r_2.
Every omitted physical level is bounded by the inherited oscillator-counting
reference tail with multiplicities binom(3N+q-1,q), q=2,...,N. These are not
hard-core physical shell multiplicities; any excess positive tail terms are
safe. No omitted low state is assumed away.

All denominator inputs are independently bounded using their own smaller
geometry data. No numerator third moment or enlarged residual enters them.
The prior implementation loads an unused largest old polynomial when imported;
that module initialization does not enter this certificate's scalar inputs.

## Joint affine energies and all-size propagation

For each interval, form the affine combinations

    J1 energy: 8 rho16 - 2 rho64,
    J2 energy: 16 rho16 - 4 rho64,
    C0 energy: 4 rho32 - 2 rho64.

Each is minimized at common coupling endpoints. Extensive constant energy
shifts cancel exactly. The independently bounded denominator traces and
single largest numerator yield directed rational J1,J2,C0 initial bounds.
The existing temperature-first/canonical coupled bootstrap then propagates
component purity and same-base joint-product information. Its proof is the
reviewed joint_ratio_review/GENERAL_LEMMA.md; its implementation is reused
without alteration. Saved bootstrap states, rational exponential bounds,
finite-window details, temperatures, and spatial scales are all replayed.
There is no reuse of a joint product at the wrong spatial base.

Every new interval starts windows at L=8, joins them consecutively to the
small-defect bootstrap, and checks the analytic large-size bound. All L=2,...,7
use the inherited q=1 reference versus the vacuum Rayleigh upper zero. L=2
has edge-square sum 16, rather than the simple-graph value 8; L=3,...,7 have
edge-square sum 2L^2. Endpoint use here follows monotonicity of this explicit
reference formula, not physical-gap monotonicity. The certificate's minimum
includes every short size, every necessary finite window, and the analytic
tail. Rational adjoining endpoints certify the whole continuous union.

## Reproduction, tests, and limitations

certify.py starts at width .001 and bisects only intervals whose bounded
beta-grid proposal cannot produce the requested .002 minimum. Seven accepted
intervals resulted. The two rejected coarse widths are only bounded-search
failures; they imply no physical or method-wide obstruction. Initial feasibility
used [.0899,.09] and gave .022821404973. Full coverage cost ~8.6 seconds and
~83 MiB. All numerical processes pin one CPU, BLAS1 and a 1 GiB address-space
cap. Reproduction reads existing exact geometry rather than recomputing costly
physical contractions. Earlier producer files and independent seals remain
unchanged. No root files, Git metadata, or remote publication are modified.

replay.py forbids eigensolvers, reconstructs every saved certificate, checks
exact matrix evaluations at interval endpoints and centers, verifies the .10
matrix, preserves the prior full [0,.085] freeze, and rejects deliberate
corruption of coefficients, affine bounds, traces, multiedges, windows and
retained-state counts. The manifest binds all scripts, exact inputs, results,
and inherited reviews. These are producer verification tests, not a substitute
for the requested independent new-interval review.
