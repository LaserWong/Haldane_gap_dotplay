# Spin-2 streamed Chebyshev heat trace: error and integer audit

Updated 2026-10-10, UTC. Scope: the isotropic spin-2 periodic Heisenberg chain
H_L(theta) = sum S_j . S_(j+1), coupling one, L=3,...,10, and seam phases
z=1,-1,omega, omega^2+omega+1=0. The target is
Z_L = Tr exp[-8(H_L+a L)], initially a=5951/1250.
This is a finite heat-trace algorithm and error proof. **No new uniform spin-2
gap or complete L9/L10 input is asserted.** A second-worker audit is pending.

## 1. Contractive Hermitian matrix

Each spin-2 bond has largest eigenvalue 4. A three-site open path is
S_2 . (S_1+S_3); its smallest eigenvalue is -10, attained by endpoint spin 4
and total spin 2. Translated two-bond inequalities imply H_L >= -5L for L>=3.
For L>=8 the archived open-eight positive-vector certificate proves
E_open8 >= -1066059959/31250000. An integer-spin SU(2) multiplet contains M=0,
so verifying the entire M=0 block bounds the full open cluster. Every path
crossing the seam can be gauged to an untwisted path. Summing translated
seven-bond inequalities gives H_L/L >= -1066059959/218750000 > -39/8.
These statements require the archived open-eight witness, not an assumed gap.

Use b=5 for L<8 and b=39/8 for L>=8, and
P = I-(H_L+bL)/64. Its spectrum lies in [1-(b+4)L/64,1], inside [-1,1]
for every supported L. Thus ||T_k(P)||<=1 and ||U_k(P)||<=k+1.
F=exp[256(P-I)]=exp[-4(H_L+bL)], and
Z_L=exp[x] ||F||_F^2, x=8L(b-a)>0.

## 2. Positive exact Chebyshev coefficients

Let X,Y be independent Poisson(128) variables. The characteristic function of
X-Y is exp[256(cos(t)-1)]. Hence, for x=cos(t),
exp[256(x-1)] = sum_(k>=0) b_k T_k(x), where
b_0=Pr(X=Y), b_k=Pr(|X-Y|=k), k>0. All coefficients are nonnegative and sum to 1.
This identity also follows directly by multiplying the two absolutely convergent
power series for exp(128 exp(it)) and exp(128 exp(-it)).

Condition X,Y to be <=J=320. Write
w_j=128^j J!/j!, S=sum_(j=0)^J w_j, and
B_k=(2-delta_k0) sum_(j=0)^(J-k) w_j w_(j+k).
Then B_k/S^2 are the exact conditional coefficients, whose sum is one.
The unnormalized Poisson tail divided by its finite sum is at most
 tau = [128^(J+1)/(J+1)!] / [(1-128/(J+2)) (S/J!)].
For any |f|<=1, conditioning one variable changes its expectation by at most
2 Pr(X>J) <=2 tau. Conditioning both changes it by at most 4 tau. Therefore
the unconditioned and conditional Chebyshev sums differ uniformly by <=4 tau.
This argument works for every real x in [-1,1] and for the associated self-adjoint P.

Take Q=2^56, choose K=141 with sum_(k>K) B_k/S^2 <1/(4Q), and set
c_k=floor(Q B_k/S^2), k<=K. The exact regeneration checks 4 tau<1/(4Q).
The final nonzero coefficient is k*=136; there are 137 nonzero coefficients,
and sum c_k=Q-74. Positivity gives the sharper combined bound
 ||F - q(P)|| <=4 tau + (1-sum c_k/Q) <75/Q,
 q(P)=sum_(k=0)^136 (c_k/Q) T_k(P).
It covers truncation, normalization, and every coefficient floor; none is omitted.
The legacy metadata's sub-1/Q bound excluded coefficient quantization and must
not be read as the total implemented polynomial error.

The exact weighted recurrence factor is
 A=sum c_k k(k+1)/(2Q)=302596763174816645/2251799813685248
   =134.37995746149085... . Its displayed decimal is not used for acceptance.

## 3. Ring, conjugate embeddings, and a useful parity invariant

Represent a coordinate as a+b sqrt(6)+(c+d sqrt(6)) omega. The kernel's sparse
integer matrix is 512P. On a bond the off-diagonal exchange magnitudes are
2,3,sqrt(6). With g(w)=(-1)^(number of sites with m=0), changing sqrt(6) to
-sqrt(6) is exactly conjugation by the diagonal sign matrix G. Indeed, a local
central ladder move changes g and an outer ladder move does not; precisely the
mixed pairs have a sqrt(6) coefficient. Changing omega to its conjugate is
complex conjugation of H. Every algebraic embedding of P is consequently
unitarily/antiunitarily equivalent to the physical Hermitian contraction.
This is essential: small physical values alone cannot bound integer coefficients
in a real quadratic number field.

For a column seeded at word v there is also an exact invariant. At row w,
only a,c can be nonzero if g(w)=g(v); only b,d can be nonzero otherwise.
Sparse multiplication, subtraction, integer multiplication, and coordinate
flooring all preserve it. In particular, the coefficient of sqrt(6) in each
squared coordinate norm vanishes exactly, so **every reported n1 must be zero**.
There is no uncontrolled cancellation of a huge quadratic irrational total.

If alpha,gamma in (-1,0], then
|alpha+omega gamma|^2=alpha^2-alpha gamma+gamma^2<=1
by convexity and the four vertices. The parity invariant therefore bounds one
physical coordinate-floor error by sqrt(6), and a block floor error by
sqrt(6d) < eta_d, where eta_d=ceil(5 ceil(sqrt(d))/2).
This holds in every algebraic embedding. For the more general intermediate
range invariant the code uses the conservative eta'_d=ceil(7 ceil(sqrt(d))/2).
Without exploiting parity, both real and complex four-component floor errors
are <=1+sqrt(6)<7/2 in every embedding (maximize the corresponding quadratic
on the rectangle [-1,sqrt(6)]^2 for the negative embedding).

## 4. Forward recurrence and accumulation error

The integer scaled recurrence is X_0=Q e_v,
 X_1=floor_coordinates(512P X_0 /512),
 X_(k+1)=floor_coordinates(512P X_k /256)-X_(k-1), k>=1.
Floors are toward negative infinity, including negative numerators.
Let E_k=X_k-Q T_k(P)e_v. Each step introduces a vector residual rho_j of
norm <=eta_d, and
 E_k=sum_(j=1)^k U_(k-j)(P) rho_j.
Therefore ||E_k||<=eta_d k(k+1)/2, including the first-step error.

The accumulator is Y=sum_(k=0)^136 floor_coordinates(c_k X_k/Q).
Each of its 137 nonzero updates has norm error <=eta_d. Positivity gives
 ||Y-Q q(P)e_v|| <=eta_d (A+137),
and consequently
 ||Y/Q-F e_v|| <=E_d/Q,
 E_d=75+ceil[eta_d(A+137)].
The argument never replaces the weighted factor A by an unjustified unweighted
stability claim. It also includes floors of coefficient products, which a
forward recurrence needs in addition to recurrence floors.

For the comparable Taylor/Horner algorithm, conditioned Poisson(256) with
J=640 has last nonzero degree 400 and coefficient mass Q-138. The exact
normalization-tail audit gives total polynomial error <139/Q. Its 401
contractive Horner updates yield E_d^H=139+401 eta_d. The comparison kernel is
a spin-2 adaptation of the existing fixed-point Horner method, not the archival
full-matrix GMP H4 program; that older program is separately retained as a
small-case independent reference.

## 5. Exact symmetry weights and complete trace enclosure

Magnetic translation T|w>=z^(-w_(L-1))|Rw> commutes with H. Reversal and spin
inversion each turn z into z^-1, so reversal followed by complex conjugation,
and spin inversion followed by complex conjugation, preserve exact column
norms. For M<0 the representatives are dihedral word orbits with doubled
weights for +M. For M=0 spin inversion is included in the orbit itself.
The kernel checks the orbit weights sum to d (M=0) or 2d (M<0).
`count_work.py` independently counts the same orbits using Burnside's lemma.

Coordinate flooring need not commute with these symmetries. Define omitted
approximate columns by transporting each computed column using an exact
monomial unitary/antiunitary symmetry and the required phase. Their individual
error bounds are unchanged. Thus, if all selected sectors have been completed,
 N=sum_(representatives r) m_r n0_r is an exact nonnegative integer,
 ||Y_full||_F^2=N/Q^2,
 ||Y_full-F_selected||_F <= e/Q,
 e=ceil sqrt(sum_(sectors M<=0) (1 if M=0 else 2) d_M E_(d_M)^2).
Let r=floor sqrt(N). Then
 max(0,r-e)/Q <=||F_selected||_F<=(r+1+e)/Q.
With exact rational exp(x) bounds [s,u],
 s max(0,r-e)^2/Q^2 <=Z_selected<=u(r+1+e)^2/Q^2.
For Kexp+2>x, the positive Taylor sum s=sum_(j=0)^Kexp x^j/j! satisfies
 exp(x)<=s+[x^(Kexp+1)/(Kexp+1)!]/[1-x/(Kexp+2)].
If sectors are omitted, add their independently certified thermal upper bound
to the upper endpoint, and zero to the lower endpoint. An old tail certificate
must be verified for the same L,beta,a before use. Completing a subset of
columns within a low-M block does not certify its missing columns.

## 6. All integer ranges and programming checks

For each embedding, every recurrence column has norm <=Q+eta'_d K(K+1)/2.
Any partial accumulator has norm <=Q+eta'_d[A+(K+1)], bounded in turn by
Q+eta'_d[K(K+1)/2+K+2]. Recovering Eisenstein real coefficients from either
complex embedding costs at most factor 2; taking the half sum/difference of
the sqrt(6) embeddings adds no larger factor. Thus all stored signed64
coordinates have absolute value at most
 B=2[Q+eta'_d(K(K+1)/2+K+2)].
The input degree is explicitly limited to 640, L<=10, and the code requires
B<2^58. It computes the maximum absolute row sum R of the expanded integer
component matrix. Each signed128 sparse partial sum is <=R B; the code checks
R B<2^100. Every floor conversion and subsequent recurrence subtraction fit
signed64 because it additionally checks floor(RB/256)+B+2<INT64_MAX.
Coefficient products fit signed128 since c_k<=Q and coordinates<=B. Signed64
accumulation is safe by the partial-accumulator invariant, not by assuming
individual coefficient terms are nonnegative.

The squared-modulus coordinates are
 n0=a^2+6b^2-ac-6bd+c^2+6d^2,
 n1=2ab-ad-bc+2cd.
Absolute per-row bounds are 21B^2 and 6B^2. Each batch has at most 32 rows,
so its absolute partial sums are <=672B^2<2^127, since B<2^58. All products,
partial products, negations, and decimal conversions fit signed128. Final
sums use GMP. The parity invariant independently predicts n1=0.
Integer site codes are below 5^10, edges below (1+2L)5^L<2^31, and accepted
start/count values below one million, so index and loop arithmetic fits int.
The ceil-sqrt initial estimate uses floating point only to propose an integer;
an integer while-loop checks ds^2>=d, so underestimation cannot reduce a bound.

Sparse rows, four length-d vectors, and orbit data are stored; no dense d by d
matrix or column matrix is allocated. Benchmark wrappers cap each child at
2 GiB address space and 600 seconds, use a single numerical thread, save the
stdout and stderr, and atomically record completed checksummed benchmarks.
The prototype's interrupted historical compile/run is never treated as a result.
