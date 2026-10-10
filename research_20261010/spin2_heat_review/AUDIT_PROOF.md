# Independent mathematical and implementation review

Scope and hashes are fixed by README.md. All assertions below refer to those
files and the stated model, parameters, and size range.

## 1. Spectral enclosure

For spin two, one bond has maximum eigenvalue 4. For a three-site path,
coupling endpoint spin a=0,...,4 to the middle spin 2 gives energy
[j(j+1)-a(a+1)-6]/2. Its minimum is -10 at a=4,j=2. A twisted open path is
unitarily gauge equivalent to an untwisted path. Summing translated two-bond
paths gives H >= -5L for L>=3.

The open-eight witness is positive in the polynomial/Marshall basis. That
basis is diagonally similar to the orthonormal physical basis, and its
offdiagonal entries are nonpositive. The verified componentwise inequality
2H q >= 2 ell q therefore implies E_min >= ell by the positive-vector bound
for a stoquastic matrix. It was independently recomputed row-by-row, obtaining
ell=-1066059959/31250000 and minimum integer margin 839778326. Every
integer-spin SU(2) multiplet contains an M=0 state, so the M=0 lower bound is
a full-cluster bound. For L>=8, translated seven-bond paths yield
H/L >= ell/7 > -39/8.

Thus b=5 for L<8 and b=39/8 otherwise gives P=I-(H+bL)/64 with spectrum
in [-1,1] throughout L=3,...,10. Consequently ||T_k(P)||<=1 and
||U_k(P)||<=k+1. The identity F=exp[256(P-I)],
Z=exp[8L(b-a)] ||F||_F^2 is exact.

## 2. Coefficients and both omitted tails

The conditioned-Poisson construction is valid. For independent Poisson(128)
variables, the characteristic function of X-Y is exp[256(cos t-1)]. Its
real part gives the positive Chebyshev series. Conditioning both variables
to be <=320 changes expectations of bounded functions by at most 4 tau,
using the displayed geometric Poisson-tail bound tau. This holds at every
x=cos t in [-1,1]; the spectral theorem transfers it to P.

The conditional weights are positive and have mass one. After truncation
and downward quantization, coefficientwise differences remain nonnegative.
Their entire contribution is exactly the lost mass,
1-sum(c_k)/Q=74/Q, rather than just the tiny Bessel/Poisson tail. Independent
exact calculation gives 4 Q tau < 1/4 and hence ||F-q(P)|| < 75/Q.
K=141 is the conditional-tail cutoff; the last nonzero implemented degree
is 136, with 137 nonzero coefficients. The weighted recurrence factor is

A = 302596763174816645 / 2251799813685248.

The conditioned Taylor/Horner weights have lost mass 138/Q, last nonzero
degree 400, and total analytic-plus-quantization error <139/Q. There are
267 nonzero coefficients but 401 Horner steps. The producer's 401-step
rounding allowance correctly includes zero-coefficient steps.

The old <1/Q analytic estimate cannot serve as the implemented polynomial
error. The frozen corrected proof and budget use 75/Q where required.

## 3. Embeddings, parity, and recurrence

In Z[sqrt(6),omega], complex conjugation sends omega to -1-omega. The other
real embedding sends sqrt(6) to -sqrt(6). A local ladder move is central
precisely when it changes whether the site has m=0. Exactly one central
move in an exchange produces sqrt(6); zero or two produce 2 or 3. Thus the
sqrt(6) embedding is conjugation by the diagonal parity matrix
(-1)^(number of zero spins). Every embedding is a physical Hermitian
contraction up to a unitary or antiunitary equivalence.

For seed v, row w contains only rational/Eisenstein coefficients when its
zero-spin parity equals v's, and only sqrt(6)-times-Eisenstein coefficients
otherwise. Multiplication, coordinate flooring, and accumulation preserve
this invariant. It makes the sqrt(6) coefficient in every squared row norm
identically zero. Hence n1 must be zero, as observed in every audited column.

For two downward floor errors alpha,gamma in [-1,0],
|alpha+omega gamma|^2=alpha^2-alpha gamma+gamma^2<=1. Parity therefore gives
per-row error <=sqrt(6) and per-block error <=sqrt(6d). The integer
eta_d=ceil(5 ceil(sqrt(d))/2) is safe in every embedding.

The first recurrence step approximates P; later steps approximate
2P X_k-X_(k-1). Writing floor residuals as rho_j gives exactly
E_k=sum_(j=1)^k U_(k-j)(P) rho_j. Thus ||E_k||<=eta_d k(k+1)/2.
Positive c_k bound weighted recurrence error by eta_d A. The separate
floors of 137 coefficient products add 137 eta_d. Therefore
E_d=75+ceil[eta_d(A+137)] is a valid integer per-column error numerator.
No unproved stability claim or missing accumulation floor is used.

## 4. Compression, signed division, and overflow

Writing X(w)=D_v(w)U(w), with D_v=1 or sqrt(6) according to parity, gives
the exact matrix D_v^-1(512P)D_v. A sqrt(6) edge becomes 1 when its
destination is a sqrt(6) row and 6 otherwise. These are exactly the factors
used in the compressed kernels. Active-coordinate floors are unchanged,
and physical norm weights are D_v(w)^2=1 or 6.

For signed x and positive 2^b, arithmetic right shift and low-bit masking
give x=2^b h+l with 0<=l<2^b. Therefore
floor(sum a_j x_j/2^b)=sum a_j h_j+floor(sum a_j l_j/2^b), including negative
values. C++20 signed shifts and the checked GCC signed128 extension implement
these floors; the static assertions pass. The baseline's explicit correction
of signed truncation also implements floor. The fast zero-imaginary-edge
branch is just the b=0 specialization of Eisenstein multiplication, with
no changed addition order.

A uniform range bound does not require extrapolating from small tests.
Even taking d=5^10, larger than the actual maximum magnetization block,
K=640, and eta'=ceil(7 ceil(sqrt(d))/2), the frozen invariant gives

B=144115192577105384 < 2^58.

The diagonal coefficient has magnitude <=512+(40+32)L. Each of at most
2L offdiagonal entries has expanded component-row L1 norm <=96. Thus the
universal row bound R=3152 is safe for all supported sizes and twists,
including both compressed seed parities. It gives

- R*(floor(B/256)+2)+B = 1918533501182718872 < INT64_MAX;
- R*511 = 1610672 < INT64_MAX;
- R*B < 2^100;
- Q*B < 2^127;
- 672*B^2 < 2^127.

These cover partial sparse sums, high-plus-shifted-low sums, recurrence
subtraction, coefficient products, and every 32-row norm chunk. Accumulator
additions use the proved partial-accumulator invariant: scalar coefficient
positivity does not require positive vector entries. Intermediate norm
products are bounded individually; cancellation does not justify safety.
Site codes, row indices, edge counts, and accepted start/count arithmetic
also fit signed32. Fresh UBSan tests supplement these proofs.

Blocking changes neither a lane's graph nor its operations. Padded lanes
remain zero and are not counted. Exhaustive small-volume tests cover mixed
seed parity, all supported widths, nonzero starts, and incomplete batches.

## 5. Symmetries and complete thermal enclosure

Magnetic translation is T|w>=z^(-w_last)|Rw>. Reversal and spin inversion
each conjugate the seam twist; composition with complex conjugation gives
an antiunitary symmetry. Exact heat-column norms are preserved. The small
graph audit checks these exact identities on 7,647 entries; the bondwise
argument proves them for all supported sizes. M<0 orbit weights are doubled
for positive-M sectors; M=0 includes spin inversion in its orbit. Independent
closure enumeration and Burnside counting agree. Total weight equals 5^L.

Flooring need not commute with a symmetry. Transporting each computed column
by an exact monomial symmetry defines an auxiliary full matrix with the
same error bound. Hence N=sum m_r n0_r is its exact squared-norm numerator,
and full error is at most e/Q, where
e=ceil sqrt(sum d_M multiplicity_M E_(d_M)^2).

Taking r=floor sqrt(N) by exact integer square root yields the norm interval
[max(0,r-e)/Q,(r+1+e)/Q]. Positive Taylor sums and geometric tails give
rational exp(x) bounds, preserving enclosure when multiplying the squared
nonnegative endpoints. This audit independently recomputed these rational
operations and complete L3/L4 traces. Decimal displays and the producer's
tiny eigensolver diagnostics are not premises.

The archived L4 reference uses 36P_old=-4-2H and mu=144, so the exponent
is -8(H+20); P_old is contractive from -20<=H<=16. Its polynomial-basis
matrices were independently regenerated exactly. The normalized Poisson
truncation through degree 640 has trace error <=2*625*tau_old. Each saved
GMP rational interval is strictly inside the independently reconstructed
Chebyshev interval. This is an additional cross-check, not an assumed
physical input to the new enclosure; archived GMP jobs were not rerun.

## 6. Limits

The L9/L10 error budgets and work counts pass independent exact arithmetic.
No complete large trace was computed. If the actual Z<=100, thermal norm
error delta implies squared-norm error <=20 delta+delta^2. This explains
the budget's stated condition but does not discharge it. Missing columns
in a low-M block require computation or an independent bound; an unrelated
old tail cannot fill that gap.

Benchmark files are performance observations. Scaling their compute seconds
by exact edge counts does not certify elapsed time, peak RAM, or feasibility.
Exact kernel equivalence also does not provide a resumable production
campaign. A long run needs the identity-bound atomic chunk protocol described
in README.md.
