# Continuous ordinary-bilayer intervals from ground states only

2026-10-10 14:51 America/New_York (EDT) / 18:51 UTC.

**Status: exact candidate; independent review pending.** The scalar arithmetic
has passed a second producer replay from frozen integer vectors with no
eigensolver calls. This is not an independent physical or analytical review.

## Result and normalization

For the ordinary spin-1/2 square bilayer with rung coupling 1, equal straight
intralayer couplings g, no crossed bonds, and positive-direction periodic bonds
counted with multiplicity, sixteen adjoining closed intervals cover

    0 <= g <= 7/100.

The candidate certifies a unique finite-volume ground state and the uniform gap

    gap(H_L(g)) >= 486442811 / 250000000000 = 0.001945771244

for every integer square side L >= 2 and every g in this interval. At g=0 the
exact gap is 1; that special value is not needed to fill any hole in the coverage.
This is a sufficient bound, not a physical phase boundary or a claim of an
optimal method threshold.

The seed patches have 16,32,64 rungs (32,64,128 physical spins), full dimensions
4^16,4^32,4^64, and fixed trial-basis dimensions 11,29,29. The two denominator
patches each retain exactly one certified ground level. The largest numerator
uses exactly one arbitrary Rayleigh trial direction; no largest residual,
second moment, lower spectrum, excited band, or completeness certificate is
required. These counts are not MPS bond dimensions.

## 1. Fixed physical bases and exact parameter polynomials

The physical Hamiltonian is shifted by the singlet-product energy:

    H'(g) = H(g) + 3N/4 = Q + g V.

Use the previously audited, g-independent B,L ground trial basis, consisting
of q=0,2,4 singlet directions. Its metric G and common removed factor 2^N are
constant. The first-moment matrix K(g) has degree one; the full second-moment
matrix J(g)=W*H'(g)^2 W has degree two:

    K(g)=K0+g K1,
    J(g)=J0+g J1+g^2 J2.

The full H action, including leakage outside the trial basis through q=6,
is already included in the audited geometry-contracted J. J is not replaced by
K G^-1 K. Only the 4x4 and 8x4 models contain J.

`build_models.py` recovers polynomial coefficients by exact rational Lagrange
algebra from the audited g=.03,.04,.05 small-patch matrices. The degree claim
comes from H'=Q+gV and a fixed physical basis, not from the sampled values. It
also verifies exact reproduction of every available saved coupling matrix.
Those extra reproduction checks are diagnostics; the proof does not assume
independent acceptance of later g=.07,.08,.10 certificates. The 8x8 model is
extracted solely from the minimal G/K files at g=.03,.04, with further minimal
file consistency checks. No largest H2 artifact is opened by this extraction.

For each interval, a small 11x11 or 29x29 generalized eigensolver proposes an
integer coefficient vector c at the rational midpoint. It is then fixed over
the entire closed interval. The eigensolver's accuracy has no evidentiary role.
The accepted norm is the exact positive integer c*G c. Division by that norm
gives an affine Rayleigh polynomial rho(g) and, on the two smaller patches,
a full residual polynomial

    r^2(g) = <H'(g)^2> - rho(g)^2 = r0+r1 g+r2 g^2.

Exact checks r0>=0, r2>=0 and 4 r0 r2>=r1^2 verify the two-operator covariance
matrix is positive semidefinite. In particular the variance polynomial is
convex, so its maximum on [a,b] is attained at an endpoint. All vectors and
rational coefficients are embedded in the interval records.

## 2. Parity refinement of the quadratic reference

The independently reviewed quadratic comparison gives, on the finite physical
hard-core subspace P,

    H' >= P L P,
    U L U* >= E_b + delta Q_ref,
    delta=sqrt(1-4g), alpha=1-2g,
    E_b= -v/(alpha+delta), v=(3g^2/4) S,
    S=sum over unordered rung edges of w_e^2,

for 0<=g<1/4. All shells of the full equal-frequency reference have multiplicity
C(3N+q-1,q). The full ordered min-max statement gives lambda_2(H')>=E_b+delta.

The same comparison restricts to even or odd total triplet parity. Here is the
extra point needed for the ground-only Temple improvement:

1. Pi=(-1)^Q is a symmetry of the physical Hamiltonian, the hard-core P, and L.
   The pair terms change number by two; number-preserving terms change it by zero.
2. The orthogonal mode rotation used in the reviewed proof preserves Q and Pi.
3. In the oscillator coordinate representation, Pi acts by f(x)->f(-x).
   Each positive oscillator dilation commutes with this reflection. Thus the
   entire finite-mode Bogoliubov unitary U preserves Pi. Equivalently its
   squeezing generator is quadratic in pair creation/annihilation, hence even.
4. Restricted form-domain min-max therefore compares the physical even sector
   to the full even reference sector, and similarly for odd parity. The first
   even reference energy is E_b, its second is E_b+2delta, and the first odd
   energy is E_b+delta. No odd reference state is inserted into the even count.

Each denominator trial is even. The interval computation explicitly verifies

    rho(g) < E_b(g)+delta(g)

uniformly. Thus the lowest even level is below every odd level. The second even
level is at least E_b+2delta>rho. The physical ground is therefore unique,
even, and identified by this variational trial. Applying ordinary rank-one
Temple inside the invariant even sector, with the full physical residual,
gives

    rho(g) - r^2(g)/(E_b(g)+2delta(g)-rho(g)) <= lambda_1(H'(g)) <= rho(g).

This argument does not assume the existence of a complete one-triplet low band.
Only the parity refinement is new relative to the reviewed full-reference
comparison; it is stated explicitly for independent review.

## 3. Continuous endpoint certificates, including energy cancellation

Rationalizing the square root makes the parameter dependence transparent. With
C=3S/16,

    E_b+q delta = C(2g-1)+(C+q)sqrt(1-4g).

For C+q>0 its second derivative is

    -4(C+q)/(1-4g)^(3/2) < 0.

Subtracting an affine fixed-vector rho leaves a concave function, so its
minimum on any closed [a,b] occurs at a or b. A directed rational lower square
root d<=sqrt(1-4g), verified by d^2<=1-4g<(d+10^-60)^2, gives safe lower
endpoint values because C+q>0. This establishes all uniform quantities

    m_q = min(endpoint lower bounds for E_b+q delta-rho), q=1,...,N,
    Vmax = max(r^2(a),r^2(b)),
    w = Vmax/m_2.

We require m_1>0 and m_2>0. The ground energy is >=rho(g)-w at every g.
Main patches have S=2N, since their side lengths are at least four. Period-two
multiplicities are instead handled explicitly in the short-size bridge below.

The largest trial Rayleigh energy rho_M(g) is affine and used only for a
partition-function lower bound. The correlated exponents

    h1(g)=8 rho_S(g)-2 rho_M(g),
    h2(g)=16 rho_S(g)-4 rho_M(g),
    h0(g)=4 rho_T(g)-2 rho_M(g)

are affine. Their uniform lower bounds are their endpoint minima, evaluated
as shared-g combinations. The extensive -3N/4 shifts cancel identically in
each combination. Bounding extensive energies independently is not used.

## 4. Full finite tail with only one retained level

After removing the physical ground and the single q=0 reference level, the
full ordered min-max comparison and C(4N,N)>=4^N yield the finite overcount

    e^(beta rho(g)) Z_N'(beta,g)
      <= exp(beta w) + sum(q=1,...,N) C(3N+q-1,q) exp(-beta m_q) = U_N(beta).

This uses reference boson multiplicities, not physical triplet-shell
multiplicities. The finite list through N has enough entries to dominate the
entire physical dimension; it does not assume the Bogoliubov-transformed
physical subspace lies in q<=N. Every term is nonnegative and evaluated with
outward rational exponentials. No cancellation-prone infinite-tail subtraction
is used.

On the largest patch spectral Jensen gives

    Z_M'(2beta,g) >= exp(-2beta rho_M(g)),

for the one fixed normalized trial, irrespective of whether it identifies the
largest ground. Following the reviewed reduced-input t,x,y route, define

    J1 >= exp(beta min h1) / U_S(beta)^8,
    J2 >= exp(beta min h2) / U_S(2beta)^8,
    C0 >= exp(beta min h0) / U_T(2beta)^2.

Thus the largest patch has no denominator or upper trace. Directed lower
rounding produces the saved J1,J2,C0. With F(z)=1-(1-z)^2/(2z^2), sequential
positive purities are

    a=F(J1), b=F(J2 a), c=F(C0^4 a^2 b).

Each value is checked in (0,1]. The exact adjacent-swap transport gives the
canonical x,y,time staircase

    A=a sqrt(b), B=a^2 b sqrt(c), C=a^4 b^2 c

at (8,8,2beta), with square roots and final values rounded downward.

## 5. All integer sizes, uniformly over each interval

The existing reviewed transfer positivity, doubling inequalities, canonical
three-purity bootstrap and signed-transfer finite-window interpolation are
used with these uniform inputs. Their model hypotheses hold pointwise for
nonnegative ordinary-bilayer couplings. Every scalar inequality is monotone in
the lower-purity inputs, so using interval-uniform lower inputs proves the
same conclusion simultaneously for every g in that interval.

`three_purity_certificate.replay` doubles until the common defect is at most
1/500 and proves its all-integer asymptotic bound. `finite_window_2d` checks
every preceding integer-size window [8*2^j,16*2^j]. The recorded final gap is
the minimum of the asymptotic result, all needed windows, and short-size bounds.
No gap in integer L is filled by informal interpolation of numerical samples.

For L=2,...,7, the exact edge-square sums are 16,18,32,50,72,98. At each interval
upper endpoint b, the same quadratic reference gives

    lambda_2(H'_L(g)) >= C_L(2b-1)+(C_L+1)d_b,
    C_L=3 S_L/16, d_b<=sqrt(1-4b).

The expression E_b+delta is decreasing on 0<=g<1/4, since its derivative is
2C_L-2(C_L+1)/sqrt(1-4g)<0. The singlet product gives lambda_1(H')<=0; therefore
the positive displayed lower endpoint is also a gap lower bound. This proves
all short sizes uniformly, with no assumed monotonicity of the physical gap.
At b=.07 the common short-size bound is >.637732662587.

The weakest interval [.06875,.07] starts asymptotic acceptance at L=1024;
finite windows beginning at 8,16,32,64,128,256,512 are all explicitly checked.
Its smallest window bound is >.002703641449, above its asymptotic .001945771244.
Other intervals use their own temperatures, fixed vectors and bootstrap depths.
The sixteen closed intervals share exact rational endpoints, proving the union
without untested parameter gaps. `coverage_summary.json` is the union ledger.

## 6. Reproduction, provenance, and limits

- `build_models.py`: exact fixed-basis polynomial extraction and consistency
  checks. Primary small-patch nodes are .03,.04,.05; largest nodes .03,.04.
- `certify_intervals.py`: tiny eigensolves for proposals, exact interval and
  scalar acceptance, and the interval union. No new geometry contraction.
- `replay_saved.py`: reconstructs every polynomial from saved integer vectors,
  then repeats every interval/scalar calculation without calling an eigensolver.
- `MODEL_INPUT_SHA256.json`: every numeric file read in extraction.
- `DEPENDENCY_SHA256.json`: imported scalar helpers and inherited proof entries.
- `FROZEN_MANIFEST.json`: immutable handoff hashes, excluding itself and rerun logs.

The inherited geometry review, full quadratic comparison review, reduced-input
route review, order-transport proof and finite-window theorem remain necessary
analytical dependencies. A new independent reviewer must check the added
parity argument, polynomial extraction, endpoint directions, exact outputs,
coverage and all-integer bridges before this candidate is upgraded.
