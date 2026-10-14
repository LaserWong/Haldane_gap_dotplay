# Rational interval partition certificates for the periodic TFI chain

## Model and exact formula

The Hamiltonian is H_L=-J sum_i Z_i Z_(i+1)-h sum_i X_i, with Pauli
normalization, J>=0 and the positive-direction periodic bond convention.
Thus L=2 has two bonds. Conjugating by product Z_i permits replacing h by g=|h|.
The implementation accepts exact integer/rational-string/Fraction parameters,
and dyadic L from 2 to 128; the seed cap is n<=64. No numerical input is
rationalized into a proof. No Hilbert basis or many-body eigenpair is computed.

The Jordan-Wigner partition identity uses L NS momenta k=2pi(m+1/2)/L
and L R momenta k=2pi m/L. Each one-particle energy is

epsilon(k)=2 sqrt((J-g)^2+2Jg(1-cos(k))).

For each sector start E=1, O=0 and, for each energy epsilon, set simultaneously
E'=E+w O and O'=O+w E, where w=exp(-beta epsilon).
These positive polynomials sum all even and odd occupation configurations,
without enumerating them. Multiply the selected polynomial by
exp(beta sum epsilon/2). NS selects E; R selects O when g>=J and E when g<J.
At g=J the R zero mode makes E=O, so the convention is continuous. Sum both
sector contributions. This includes beta=0 and the decoupled J=0/g=0 limits.
The physical parity justification and independent numerical verification are
in QUANTUM_ISING_SEEDS.md. The recurrence has O(L) fixed-precision operations;
it is not a low-many-body-spectrum approximation.

## Exact enclosure arithmetic

All endpoints are Python Fractions. Every addition, subtraction, multiplication
and division rounds outward onto denominator D=10^digits. A division interval
containing zero is rejected, never silently trusted. Decimal precision is
bounded to 20..100. Endpoint products are minimized/maximized exactly.
For rational x>=0, floor(sqrt(x)*D) is obtained by integer isqrt of
floor(x*D^2), with the upper endpoint increased by one unless equality holds.
No floating square root, pi, or trigonometric evaluation is used.

For cos(pi m/2^p), exact modular reduction and reflection first put the angle
in [0,pi/2]. Endpoints 0,pi/2,pi are exact. All other values follow from the
positive half-angle identity cos(theta)=sqrt((1+cos(2theta))/2). The recursion
reduces p; negative signs are applied only after reflection. Consequently the
trigonometric inputs are certified algebraic enclosures.

For exp(x), reduce |x| by an exact power of two to r<=1/2. A positive Taylor
sum through degree N has omitted tail at most twice the next term, since
all subsequent ratios are <=1/2. Interval term recurrence and outward sums
bound that term and the partial sum. N is selected using the rational bound
2*(1/2)^(N+1)/(N+1)! <=1/D. Repeated interval squaring undoes the range reduction;
reciprocal encloses negative exponents. Monotonicity extends this to interval
arguments. |x|>4096 is rejected as a resource guard. These facts, not numerical
agreement, establish the enclosures.

## Common energy shift and purity ratios

A single rational C is chosen as the midpoint of the enclosure of
sum_NS epsilon/(2L) at the largest spatial size L=2n. The code evaluates
Zhat(L,beta)=exp(-beta C L) Z(L,beta). This keeps the vacuum-normalized
partition values near one without subtracting nearly equal sector products.
C is derived solely from exact enclosures and reused in all three evaluations.
Its accuracy affects efficiency, not validity. For exactly this common shift,

S=Zhat(2n,beta)/Zhat(n,beta)^2=Z(2n,beta)/Z(n,beta)^2,
T=Zhat(2n,2beta)/Zhat(2n,beta)^2=Z(2n,2beta)/Z(2n,beta)^2.

Interval division therefore returns rigorous finite partition purity bounds.
Three partition evaluations visit 10n modes, with 6n distinct mode enclosures.
Increasing precision can resolve intervals with an unusably small denominator;
finite precision failure does not establish physical gaplessness.

## Exact target and limits of the certificate

For n=16, beta=8, J=1, h=3/2, 50-digit enclosures give display values
S=0.99586104532973856665 and T=0.99870423197679716273.
Both interval widths are below 10^-40. Exact rational lower endpoints feed the
unmodified dedicated d=1 scalar kernel with K=5 and threshold u<=1/100.
Its outward lower bound is 0.484734263212, with zero growth rounds.
Numerical display values are never consumed as proof inputs.

The return class is EXACT_RATIONAL_PARTITION_SEED_ENCLOSURES. The nested kernel
retains VERIFIED_CONDITIONAL, and neither module claims an unconditionally
verified physical theorem. [TRANSFER_ELIGIBILITY.md](TRANSFER_ELIGIBILITY.md)
supplies the separate spatial-transfer/reflection-positivity argument. The
signed all-integer interpolation and dedicated K=5 bootstrap theorem come from
the repository's [seed-size derivations](../../seed_size/proofs/DERIVATIONS.md)
and [two-dimensional theory](../../two_d_theory/THEORY.md), rather than from
transfer eligibility alone. These links are relative to this document's deployed
location under gap_workflow/theory/.
After independently accepting these physical and bootstrap hypotheses, the bootstrap scope
is L>=n (or its returned enlarged seed), not the omitted L<n rings. This module
keeps small_size_bridge_verified=false and uniform_family_claim=false. Any
separate all-size analytic TFI gap/bridge proof must be reviewed and combined
explicitly rather than silently promoted by the arithmetic result.

## Verification

The tests check exact square-root endpoint inequalities, every dyadic cosine
needed through L=128, positive/negative exponential enclosures, parity cases,
criticality, zero/negative field, beta=0, shift cancellation, rejected floats,
and resource caps. Target enclosures are compared at 100 decimal digits both
with the log-positive recurrence and with an algebraically different hyperbolic
product formula Z=(C_NS+S_NS+C_R-S_R)/2 in the g>J case. These comparisons are
independent numerical cross-checks, not independent exact proof verification.
