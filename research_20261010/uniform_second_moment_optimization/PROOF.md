# Signed second-initialization moment optimization

2026-10-10 19:29 EDT / 23:29 UTC. Uniform periodic spin-1 Heisenberg chain,
beta=49/4, shift a=700741/500000. All statements are conditional on the eighteen
published thermal integer certificates and the self-adjoint transfer identification.
This work does not rerun those physical matrices. No transfer rank, quantum
realization of a relaxed measure, or finite eigenvalue count is assumed.

## Inputs and exact interval arithmetic

`explore.py` parses the literal B table in the archived published scalar checker,
without executing it. It independently reconstructs the published scalar L,U
formulas using exact fractions and rounds them outward to 10^-18. These retain
much more of the printed information than a uniform 30e-6 error. In particular
large relative cancellation is not silently evaluated in floating point.

For n=4,...,12, J_n=(Z_n+3P_n)/4 and N_n=(Z_n-P_n)/4. The N lower endpoint uses
Z_lower-P_upper and its upper endpoint Z_upper-P_lower. Odd moments are signed;
all four odd N moments here are negative. The moment orders remain 4,...,12
in lambda, never 2,...,6 in lambda squared. J has multiplicity one and N three.
Each sector bound is valid for the same original Z,P box. Summing sector upper
bounds is conservative even with their shared Z,P correlations; no independence
or attainability of sector worst cases is asserted. Likewise different scalar
intervals may have physical correlations; enlarging to the displayed enclosure
box is safe, but cannot establish globally sharp physical bounds.

## Unit-atom Hankel / Christoffel exclusion

Let H_ij=m_(4+i+j), i,j=0,...,4, and v(t)=(1,t,...,t^4)^T.
Every occurrence of a transfer eigenvalue t has unit spectral mass; removing
one copy gives H-t^4 v(t)v(t)^T positive semidefinite. This is legitimate for
infinite rank: lambda^2 q(lambda) is square summable since m4 and m12 are finite.
Hence for every degree-four q,

    t^4 q(t)^2 <= sum_lambda lambda^4 q(lambda)^2.

For positive definite exact H, the strongest such inequality at t is

    t^4 v(t)^T H^(-1) v(t) <= 1.

This is a necessary one-unit-atom condition, not a sufficient integral-spectrum
realizability criterion. Arbitrary weighted measures would not allow subtracting
one unit atom. Numerical optimization merely proposes rational q coefficients;
all accepted results are proved by `certify.py` using fractions only.

Write q^2=sum c_j x^j. The exact interval upper bound is
B=sum c_j upper(m_(4+j)) for c_j>=0 and c_j lower(m_(4+j)) otherwise.
For each signed ray t=sign*r, the checker proves at the rational cap r0:

    r0^4 q(sign*r0)^2 > B.

It also expands q(sign*(r0+y)) exactly. Every coefficient is strictly positive.
Thus this expression and (r0+y)^4 are positive and increasing for all y>=0,
proving exclusion on the entire exterior ray, with no missed disconnected
component or reliance on a numerical root scan. The resulting open supports are

    -0.6501774659 < lambda_J < 1.0013390453,
    -0.8710299903 < lambda_N < 0.7502278231.

The old caps are |lambda_J|<1.00139 and |lambda_N|<.872. The four exact
polynomials, margins, and shifted coefficient lists are in certificate.json.

## What is near-optimal, and what is not

For the simultaneous midpoint of the scalar enclosure box, the checker
constructs H-t^4 v(t)v(t)^T and verifies strictly positive rational LDL pivots.
This occurs at t=1.001336, -.650141, .750214, -.871022 respectively. At these
points every degree-four square filter is inconclusive for that midpoint data.
Therefore a robust square-filter method using only this enclosure box cannot
exclude these t. This brackets the method's caps closely. It does not prove
that the midpoint data have a physical realization, or that they have an
integer-atom spectral realization. Other non-square constraints or additional
physical information may improve the bounds. It also does not certify global
optimization over all valid moment-based methods.

## Longer even moments and distinguished positive eigenvalue

For nonnegative y_i<=h with sum y_i<=m and r>=1, convex mass packing gives
sum y_i^r <= floor(m/h)*h^r+(m-floor(m/h)*h)^r. This passes to infinite lists
by monotone convergence. Applying y=lambda^12 gives exact longer traces for
multiples of 12. certificate.json compares the new values with the same recipe
using the official old caps and m12 upper bounds.

The published physical trial inequality supplies Z72>1. If every J eigenvalue
had modulus <=ell=.9999979746, packing would give Z72<1, by the exact positive
margin in the certificate. Thus there is an eigenvalue with modulus >ell.
Our negative J ray bound shows that eigenvalue is positive. Removing it leaves
J twelfth mass <=mJ-ell^12. Together with N packing this gives the exact initial
purity defect upper bounds recorded in the certificate, approximately
p0=.04467006818632 and q0=.17548369502741 at spatial length36, thermal length72.
These are improvements to the original p0<.047916 and q0<.181521. No new
all-size gap theorem is asserted by this package alone.

## Polynomial long-moment majorants

`long_lp.py` proposes degree-eight p such that p(x)>=x^(k-4) on the full signed
sector interval. Only the subsequent exact checker can certify a proposal.
`certify_long.py` rounds coefficients to rationals and adds a rational constant;
it proves p(x)-x^(k-4)>=0 by converting to Bernstein coefficients and recursively
bisecting with exact de Casteljau arithmetic until every leaf's coefficients
are nonnegative. Bernstein basis functions are nonnegative and sum to one, so
this is a proof over the whole interval, not a grid test. Multiplication by
x^4 and summation gives m_k<=sum p_j m_(4+j), with the same sign-sensitive exact
interval arithmetic. The final long_certificate.json records every polynomial,
upper bound, and subdivision depth. Floating LP/minimization only supplies
candidates, and is not trusted by any proof assertion.

## Reproduction and scope

Run on CPU6, with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1:

    python certify.py
    python certify_long.py

The first checker reconstructs all scalar endpoints and cap proofs. The second
reconstructs its polynomial positivity certificates. Both enforce 600 CPU
seconds and700MiB address-space limits. Search scripts are optional and only
produce candidates. No thermal jobs, full diagonalization, frozen artifacts,
root-status files, or remote repositories are modified.

## Improved continuation certificate

Combining the exact N36 polynomial bound .006938592840575 (per one N sector)
with the residual J mass bound reduces the spatial defect to
.040903345383812; the thermal defect remains below .175483695027402.
`continue_seed.py` uses this pair at (n,beta)=(36,49/4), the canonical recurrence
S_new=G(S^2*T), T_new=G(T^2*S_new), G(x)=1-(1-x)^2/(2*x^2), and directed
160-decimal rational arithmetic. Every early dyadic all-integer window is
checked at its actual temperature via the already reviewed canonical signed
interpolation lemma; roots and exponentials have exact outward enclosures.
The terminal small-defect theorem closes at n=36864, beta=12544. The resulting
producer statement is conditional gap >=107/5000=.0214, unique ground state,
for every integer physical length L>=36. It inherits the transfer identities,
all-integer interpolation, and asymptotic bootstrap from the cited accepted
proofs, plus the same eighteen published thermal data premises. It is awaiting
independent review and does not change their verification status.

The integer windows cover [36,72], [72,144], and so forth without gaps; no odd
size positivity is inferred from even traces alone. The inherited physical
all-integer thermal-trace identity is essential. At each window the exact
computed lower purity C obeys C>exp(beta*.0214)*(1-C). At the terminal state,
u=max(1-S,1-T)<=.01 and 1-5*u*exp(beta*.0214)>0. These are the positive margins
saved in continuation_certificate.json. Run `python continue_seed.py` after
the two moment certificate scripts to reproduce.
