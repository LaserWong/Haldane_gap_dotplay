# Physical inputs and uniform coupling bounds

Updated 2026-10-10 17:56 America/New_York (EDT) / 21:56 UTC.

Ordinary periodic spin-1/2 square bilayer: unit antiferromagnetic rung coupling,
straight intralayer coupling g, no crossed coupling. Use H'(g)=H(g)+3N/4
=Q+gV on N rungs, with positive-direction periodic bond multiplicities.
The result concerns square integer sides L>=2, not arbitrary aspect ratios
or uniqueness of an infinite-volume state.

The new 8x4 denominator ground witness is the single fixed rational vector
from the independently reviewed complete-residual package. It is a singlet,
even under rung triplet parity, supported in q=0,2,4,6, with complete H'
action through q=8. Its search dimension is 43; full Hilbert dimension is
2^64. We reuse its accepted exact norm, affine mean rho32(g), and quadratic
full second moment. The exported full variance v32(g) is the second moment
minus rho32(g)^2, not a projected residual. Its exact positive-semidefinite
quadratic test is checked on import. No q8 enumeration or new physical
contraction is performed here. The physical, polynomial and independent
review hashes are required explicitly in manifest.py.

The 4x4 denominator keeps its fixed-center 11-dimensional auxiliary vector,
complete residual polynomial and existing odd translated family. The 8x4
odd translated family is also unchanged. The numerator is one 8x8-rung
state from the accepted coupling-independent 43D basis. Its mean is affine;
its 128-spin Hilbert dimension is 2^128. No largest-patch residual is used.
The matrix identity at g=.10 is checked against the independently constructed
point input, as in interval_range_009/PROOF.md. Search dimensions, respectively,
are 11,43,43; denominator retained counts remain 49 and 97, and the largest
numerator retained count remains one. Available ground-plus-odd trial spaces
have dimensions 59 and 139, not those retained-state counts.

For each closed interval [a,b], all three witnesses are fixed. Only the 4x4
and 8x8 coefficients are proposed at its midpoint; the 8x4 complete witness
is the same throughout [.09,.10]. Exact endpoint values give:

r_q(g)=(3N/8)(2g-1)+(3N/8+q)sqrt(1-4g),

D_q=min_{g=a,b}(directed lower r_q(g)-rho(g)),
Vmax=max(v(a),v(b)).

The exact reference is concave and rho is affine, so D_q is a valid lower
bound everywhere, using a 60-decimal rational lower square root at endpoints.
The full variance is convex, so Vmax bounds it everywhere. Two separate
conditions are checked: D_1>0 establishes a unique global ground state,
while D_2>0 permits Temple in the even singlet sector. That sector has only
one vacuum state below the q=2 reference cutoff. Thus

rho(g)-Vmax/D_2 <= E0'(g) <= rho(g)

uniformly. The stronger even-sector cutoff is not silently substituted for
the separate global uniqueness condition.

Odd-mode first moments and complete variances are the previously reviewed
fixed-center affine and convex-quadratic polynomials in Q(sqrt(2)). Directed
160-bit endpoint enclosures provide uniform Temple denominators and lower
energies relative to the current ground rho(g), including the new 8x4 rho.
The exact dimension count keeps ground plus 3N odd levels below r2. Omitted
levels are bounded by the inherited bosonic reference tail, multiplicities
binom(3N+q-1,q), q=2,...,N. These multiplicities are not hard-core dimensions;
overcounting adds nonnegative upper-tail terms. Nothing discards omitted
states on the strength of a small residual.

This argument uses convexity/concavity and exact operator-affinity identities,
not physical-gap monotonicity or interpolation between successful points.
