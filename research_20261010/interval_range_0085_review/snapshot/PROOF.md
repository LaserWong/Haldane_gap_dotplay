# Continuous ordinary-bilayer extension through g=.085

Updated 2026-10-10 15:35 America/New_York (EDT, UTC−4) / 19:35 UTC.
Status: exact producer certificate, awaiting independent interval and new
fixed-center polynomial reconstruction review.

## 1. Result and unchanged scope

For the ordinary periodic spin-1/2 square bilayer with unit rung coupling,
nonnegative straight intralayer coupling g, no crossed bonds, and the inherited
positive-direction periodic bond multiplicities, sixteen adjoining closed
intervals cover [.08,.085]. Every real coupling in this range and every integer
square side L≥2 has a unique finite-volume ground and the uniform lower bound

    gap(H_L(g)) ≥ 1682875193/500000000000 = .003365750386.

The first seven intervals cover [.08,.082] with only a single ground-level
contribution on each patch, giving at least .005978179134. The remaining nine
cover [.082,.085] and add the audited translated triplet families on the two
smaller denominator patches, giving at least .003365750386.

Joining the unchanged three earlier producer freezes yields 49 closed pieces
covering [0,17/200] and preserves their smaller uniform lower bound

    gap(H_L(g)) ≥ 486442811/250000000000 = .001945771244.

The new sixteen pieces remain candidates until their independent audit passes.
The combined claim inherits the earlier physical and scalar reviews, including
the separate [.078,.08] acceptance. Exact adjoining endpoints are checked;
there is no interpolation of finitely sampled physical gap values.

These are sufficient certificates, not optimal thresholds or estimates of the
actual gap. No assertion concerns arbitrary aspect ratios, uniqueness of all
infinite-volume ground states, or a physical critical coupling. The local tree
is an extracted snapshot without Git metadata; no commit or remote publication
is claimed.

## 2. Preserved ground-only route

The proofs of the exact ground matrix polynomials, even-sector Temple bound,
full bosonic reference, uniform implicit filter, correlated affine energies,
and joint scalar propagation are exactly those of interval_extension/PROOF.md,
interval_extension_review/REVIEW.md, interval_joint_extension/PROOF.md, and
joint_ratio_review/GENERAL_LEMMA.md. Their hashes and review seals are explicit
inputs. No earlier frozen file is edited.

The fixed ground basis W is g-independent and H′(g)=H(g)+3N/4=Q+gV. Thus its
Gram matrix is constant, first moment affine, and complete second moment
quadratic. These are identities following from fixed W and affine H′, rather
than empirical fits. Every original source at .03,.04,.05,.06,.07,.08,.10 is
checked against the exported matrices.

Each denominator uses one fixed rational vector c, with affine Rayleigh
normalizer rho(g) and full quadratic residual v(g). The q=1 reference cutoff
above rho identifies the unique full-space ground; parity gives the q=2
cutoff for Temple. Concavity of the reference minus an affine rho bounds it
below by the lesser endpoint. The nonnegative quadratic variance is convex,
so its maximum is the larger endpoint. This yields a uniform width w and
rho(g)−w≤lambda_ground(g)≤rho(g).

For the first regime the existing .08 auxiliary vectors are reused. In the
second regime an 11×11 or 29×29 floating generalized eigenproblem merely
proposes a new integer auxiliary vector at the interval center. Its proposed
eigenvalue and pencil endpoint are never accepted as spectral inputs: the
saved vector is evaluated from exact polynomial G/H/H² and the same uniform
Temple proof. Exact replay forbids eigensolver calls.

The largest 8×8-rung patch uses just the prior one-vector implicit filter. For
a fixed base psi, full residual variance v, upper residual compression Rmax,
and Cmax=Rmax−min rho, let t=1/Cmax and

    d=vmin Cmax/(Cmax²+vmin).

The family (psi−t(H′(g)−rho(g))psi)/sqrt(1+t²v(g)) has Rayleigh quotient at most
rho(g)−d. The quadratic minimum vmin includes the rational interior vertex
when present. This monotone-fraction bound retains the normalization and
negative numerator together. No residual for the filtered family is claimed.
Only G/H/H² of the original fixed ground basis is read, including complete
q=6 leakage. No H³/H⁴, new sparse support, or maximum-patch diagonalization is
performed. The largest odd/triplet moment input is never needed.

## 3. Analytic odd-family degree and normalization

The literal audited trial definition in translation_band/translated_band.py is

    w_r(z)=u_r+z v_r,
    u_r=|t+_r>,    v_r=−C_create(1)|t+_r>/2.

The creation operator is explicitly the part of V raising triplet number by
two. The implementation adds only q=3 entries of T applied to the bare q=1
state. Consequently Qu_r=u_r and Qv_r=3v_r exactly. This is stronger than a
statement that their sum happens to be supported in q=1⊕q=3; v_r has no q=1
part. Q and translations commute, and the physical metric is fixed.

For each displacement r, the coupling-dependent diagonal-family moments obey

    G(z)=<w_0(z),w_r(z)>                         degree ≤2,
    A(z)=<w_0(z),H′(z)w_r(z)>                   degree ≤3,
    B(z)=<H′(z)w_0(z),H′(z)w_r(z)>              degree ≤4.

These degree bounds follow analytically from affine w and affine H′. They are
not inferred from finite-point agreement. Orthogonality of Q eigenspaces gives
G(z)=G0+z²G2, with no linear coefficient.

At each source coupling z=p/q, the saved producer uses d=4q, T=dH′(z), and
W_r=2d w_r(z). Hence divide its stored displacement arrays by 4d², 4d³, and
4d⁴ for G,A,B respectively before any polynomial extraction. The geometry's
fixed inner-product normalization is preserved. Interpolating the raw integer
arrays without these factors would be incorrect.

The seven already audited source couplings determine each known-degree
polynomial by exact rational Lagrange interpolation; every remaining coupling
is verified exactly. For the two denominator geometries this gives 1,008 exact
source evaluations, of which 432 are beyond the degree+1 defining values.
No new physical vector or Hamiltonian action is constructed.

## 4. Bivariate reconstruction for a fixed trial center

Now keep the trial center z fixed and vary the physical coupling p. Put

    Qmom(z)=G0+3z²G2,
    Q2mom(z)=G0+9z²G2,
    Vmom(z)=[A(z)−Qmom(z)]/z=v0+z v1+z²v2.

The quotient is a polynomial identity, including its continuation at z=0.
The mixed second-moment polynomial is

    C(z)=<Qw_0,Vw_r>+<Vw_0,Qw_r>
        =2v0+4z v1+6z²v2.

For a left Q eigenvector of eigenvalue qi and right Q eigenvector of eigenvalue
qj, the first term contributes qi<w_i,Vw_j>, while Hermiticity of V moves the
second term to qj<w_i,Vw_j>. Thus the weights are qi+qj=2,4,6 for the constant,
linear, and quadratic terms. This applies separately to each cross-displacement
matrix element; it does not assume that the two cross terms are equal or real.
The saved real displacement arrays additionally satisfy inversion/Hermitian
symmetry, which is checked coefficient by coefficient.

Define the degree≤2 polynomial

    D(z)=[B(z)−Q2mom(z)−z C(z)]/z².

The constant and linear numerator terms vanish identically. For the fixed
family w_r(z), the exact moments at any physical coupling p are therefore

    G_fixed(p)=G(z),
    A_fixed(p)=Qmom(z)+p Vmom(z),
    B_fixed(p)=Q2mom(z)+p C(z)+p²D(z).

The implementation checks the vanishing terms, full diagonal recovery at
p=z, exact source normalization, displacement symmetry, and additional direct
rational Hermitian-matrix fixtures with distinct left/right columns. These
fixtures support implementation testing; the operator identities supply the
all-real-p proof.

## 5. Fourier modes and uniform odd Temple endpoints

Translations diagonalize the circulant Gram/first/second moments. Side lengths
divide eight, so each Fourier symbol belongs exactly to Q(sqrt(2)). The Gram
symbol is strictly positive for every mode at the fixed center. Its positive
normalization gives affine theta_k(p), quadratic second moment, and quadratic
full variance v_k(p). Exact Q(sqrt(2)) signs check nonnegative constant and
quadratic variance coefficients and the covariance determinant. Thus v_k is
nonnegative and convex on the full real line.

Let a2(p)=E_b(p)+2 sqrt(1−4p) be the reviewed global next-band lower cutoff.
For N=16,32 the reference is

    E_b(p)+q delta(p)=C(2p−1)+(C+q)sqrt(1−4p), C=3N/8.

This is concave for p<1/4. For each interval [a,b], define exact rational lower
bounds and upper bounds

    m_k=min_endpoints [a2(p)−theta_k(p)] > 0,
    V_k=max_endpoints v_k(p),
    w_k=V_k/m_k,
    ell_k=min_endpoints [theta_k(p)−rho_ground(p)]−w_k.

Square roots of 1−4p use certified downward rational bounds; Q(sqrt(2)) uses
160-bit directed enclosures. The endpoint formula for m_k is valid by
concavity, and V_k is valid by convexity. The last affine difference is bounded
jointly at common endpoints, preserving correlation with rho_ground.

Every mode is below a2 throughout the whole interval. The translated vectors
retain total spin one because the pair-creation operator is an SU(2) scalar.
Thus each momentum supplies three orthogonal spin components and the complete
odd trial space has dimension 3N. Together with the even ground trial, all
1+3N trial directions have Rayleigh spectrum strictly below a2. The complete
bosonic comparison gives lambda_(3N+2)≥a2. There are therefore exactly 1+3N
physical levels below a2, including exactly one in each indicated spin/momentum
sector and the unique even global ground. No additional low eigenstate is
assumed away. Rank-one Temple within each such sector yields

    lambda_k(p)−rho_ground(p) ≥ ell_k

uniformly. The proof needs complete H² moments, not a compressed square of the
first-moment matrix.

## 6. Full trace denominator and preserved numerator

The reviewed reference has oscillator multiplicities d_q=binom(3N+q−1,q).
Its q=0,1 multiplicities are exactly 1 and 3N. Replace precisely these entries
by the certified ground and full odd band; retain q=2,…,N for every other
physical eigenvalue. Since sum_(q=0)^N d_q=binom(4N,N)≥4^N, adding any excess
positive reference terms is safe. This does not identify oscillator counts
with hard-core triplet-shell dimensions.

For each denominator patch the uniform normalized trace upper is

    exp(beta rho_ground(p)) Z′_N(beta,p)
      ≤ exp(beta w_ground)
        +3 sum_k exp(−beta ell_k)
        +sum_(q=2)^N d_q exp(−beta m_q),

where m_q=min_endpoints [E_b(p)+q delta(p)−rho_ground(p)].
Ground-only intervals retain the original q=1,…,N tail instead. The largest
numerator has only the single filtered Jensen contribution. Correlated affine
energies 8rho16−2rho64, 16rho16−4rho64, and 4rho32−2rho64 are minimized at common
coupling endpoints; extensive ground-energy shifts cancel identically.

Directed rational exponential evaluations and downward 18-decimal ratio
rounding give the same txy initial ladder as the reviewed earlier route.
The independent same-base joint-product bound is preserved through coupled
txy/canonical continuation and every joint-aware finite window, exactly as
specified by the accepted GENERAL_LEMMA. Component labels, spatial lengths,
beta, and joint K are all recorded; an old-base K is never reused at a new base.

## 7. Every integer size and union

There are 100 saved coupled ladder states and finite windows, plus 96 small-size
rows for L=2,…,7. Every interval starts its finite windows at L=8. All required
consecutive windows are positive until the canonical common defect enters the
reviewed domain ≤1/500, at most L=1024. The unchanged analytic small-defect
theorem then covers every larger integer size. Each rational gap is checked
with directed exponentials rather than an unverified floating logarithm.

The short-size bound is the ground vacuum Rayleigh upper zero and the reviewed
q=1 comparison at the interval's upper coupling endpoint. At L=2 the exact
edge-square sum is 16; at L=3,…,7 it is 2L². The comparison bound is monotone in
the required direction; physical-gap monotonicity is not assumed.

The final bound for each coupling interval is the minimum of its short-size
bound, all required finite windows, and the analytic tail. Shared rational
endpoints cover the entire coupling union. replay_saved.py verifies every
saved rational input, each complete certificate, the two new contiguous
regimes, all earlier producer freezes, and the [0,.085] union without an
eigensolver call.

## 8. Inputs, dimensions, and resource cost

The physical seed patches remain 4×4, 8×4, and 8×8 rungs: 32/64/128 spins and
full Hilbert dimensions 2^32/2^64/2^128. Ground search dimensions remain
11/29/29; the largest ground search augmented by its one implicit direction
has dimension at most 30, and its filtered state has q≤6.

For [.08,.082], each trace uses one ground contribution; the corresponding
available ground/filtered spaces have dimensions 11/29/≤30. For [.082,.085],
the denominator trace retained-state counts rise to 49 and 97, comprising one
ground plus 48 and 96 odd states. Their odd linear spaces have dimensions 48
and 96. If combined with the original ground search spaces, the available
linear spaces have dimensions 59 and 125; these are not MPS bond dimensions.
The actual fixed ground witness and odd family span 49/97 directions on each
interval, while the largest numerator still contributes only one state at
each coupling. No odd moment is consumed on the largest patch.

Odd trial support is q=1,3 and its full H image is q=1,3,5. These are existing
moment data with an exact fixed-center reconstruction, not newly enumerated
large sparse support. The ground-only proposal used about 13.4 seconds and the
odd extension about 38.9 seconds. Every production/replay process pins one CPU,
sets numerical library threads to one, and has a 1 GiB address-space cap.

The bounded ground-only beta5…30 step.05 diagnostic failed at .083,.084,.085,
including a check using the .085 auxiliary vectors. This is not a proof that
all beta, other vectors, or other scalar schemes fail. It merely motivated
using the already available denominator odd-band information.

Run REPRODUCE.sh from this directory or repository root. Hash verification
precedes source checks, exact saved replay, and filter/joint/polynomial tests.
All new work is confined to interval_range_0085; earlier freezes are preserved.

## 9. Final producer verification

The complete final reproduction passed in 19.05 seconds with 85,296 KiB peak
child RSS (about 83.3 MiB). It verifies 96 direct input hashes and all 1,165
files in ten inherited independent-review seals. The 36 direct cross-column
bivariate fixtures, 720 diagonal-recovery checks, 432 exact covariance checks,
3,888 supplementary within-interval checks, filter and joint diagnostics, and
19 deliberate replay/trace corruption guards all passed. These are producer
checks and do not replace the pending independent new-interval review.
