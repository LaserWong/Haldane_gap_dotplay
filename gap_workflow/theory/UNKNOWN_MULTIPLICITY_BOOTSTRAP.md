# Unknown ground multiplicity: finite certificates and bootstrap boundaries

## Result

Ground multiplicity need not be an input. Exact full-space spectral counts,
together with a distinct-root separation bound, can infer it. In particular,
a counted bottom cluster narrower than that separation is an exact ground
space. This is a finite-matrix theorem with a checkable strict inequality.
It does not provide a new spatial bootstrap or a volume-uniform gap by itself.

A low-temperature purity plateau near 1/r can instead reflect r almost
coincident levels with a unique ground state. Cooling a fixed matrix,
refining an enclosure, and increasing the physical volume are different
operations; exchanging them is the central invalid inference to avoid.

The proofs below are elementary and self-contained. Relevant local sources
are THEORY.md Sections 1, 2, 6, and 7; DEGENERATE_PURITY.md Sections 1--3;
and gapflow/low_band.py. No numerical eigensolver or external theorem is
being used as evidence for an exact degeneracy.

## 1. Counted cluster certificate, without a ground-rank assumption

Let H be a D-dimensional Hermitian matrix, with ordered eigenvalues
E_0 <= ... <= E_(D-1), including multiplicities. Assume full-space evidence
(including all symmetry sectors) proves, for a < b < t,

    a <= E_0 <= ... <= E_(r-1) < b < t <= E_r,
    1 <= r < D.

Set w=b-a and gamma=t-b>0. Exact inertia at a,b,t can prove this statement;
a threshold eigenvalue at t is allowed. Let g denote the actual, initially
unknown, multiplicity of E_0. Then g<=r. The certificate proves

    E_r-E_(r-1) > gamma,
    E_r-E_0 > gamma,

but it does not in general prove that the true gap Delta=E_g-E_0 exceeds
gamma. If g<r, that true gap is inside the cluster and is less than w.
If g=r, the external separation is a true ground-space gap.

A known lower bound s on every eigenvalue multiplicity is an alternative:
if r=s then g=r. This requires an actual full-space symmetry theorem,
not a numerical degeneracy tolerance. The special Kramers case s=2
therefore resolves a rank-two cluster only after its antiunitary hypotheses
have been proved.

## 2. What the same cluster proves thermally

Let rho_beta=exp(-beta H)/Z(beta), and let q be its probability outside
the bottom cluster. The retained partition sum is at least r exp(-beta b),
while the omitted sum is at most (D-r) exp(-beta t). Consequently

    q <= A/(1+A),   A=((D-r)/r) exp(-beta gamma).

This controls the entire omitted space without knowing g. Let sigma be the
normalized Gibbs state inside the cluster. The r retained unnormalized
weights differ by at most exp(beta w), so

    1/r <= Tr(sigma^2) <= min(1, exp(2 beta w)/r).

The upper bound follows by bounding each normalized probability by
exp(beta w)/r and summing its square; it is deliberately conservative.
With tau the normalized omitted state,

    T(beta) = Tr(rho_beta^2)
            = (1-q)^2 Tr(sigma^2) + q^2 Tr(tau^2).

Since both purities lie in [0,1],

    |T(beta)-1/r| <= (exp(2 beta w)-1)/r + 2q.

Thus a window with beta*w small and A small proves a thermal rank-r
plateau, not exact ground rank r. This is a useful certificate of thermal
concentration in an isolated band. Neither the rank nor this estimate
requires all retained levels to coincide.

Counterexample: H_epsilon=diag(0,epsilon,1), 0<epsilon<1/4. Take
a=0, b=2 epsilon, t=1, r=2. Then w=2 epsilon and gamma=1-2 epsilon,
but g=1 and Delta=epsilon. In the window

    1 << beta << 1/epsilon,

T(beta) is close to 1/2. For any bounded range of beta, its partition
functions and purities approach those of diag(0,0,1) as epsilon->0.
Hence finite-temperature observations with nonzero error tolerance
cannot universally distinguish these two ground multiplicities.
This statement does not exclude exact symbolic reconstruction from a
sufficiently informative finite dataset.

## 3. Explicit arithmetic separation for rational finite matrices

Suppose H has rational entries, or is represented by the rational definite
pencil A-xW with A=A^T and W=W^T>0. Form its characteristic polynomial
(or det(A-xW)); remove repeated polynomial factors over Q and clear
denominators to obtain a squarefree polynomial

    p(x)=c x^m + a_(m-1) x^(m-1) + ... + a_0 in Z[x], c>0.

Its roots are precisely the distinct physical energies. An exact complete
sector decomposition can instead use the squarefree least common multiple
of sector polynomials. Sector multiplicity weights still belong in the
inertia counts, even though each distinct root appears only once here.

For m=1, all states have the same energy and there is no excited space.
For m>=2, choose a certified R>0 containing every root in [-R,R]; for
example

    R = 1 + max_(k<m) |a_k/c|.

Proof of this root bound: for |x|>1+M, with M=max|a_k/c|,
the sum of the lower terms has absolute value less than
c M |x|^m/(|x|-1) < c |x|^m, so p(x) cannot vanish.

Put N=m(m-1)/2 and define

    rho = c^(-(m-1)) (2R)^(-(N-1)) > 0.

Every two distinct roots have distance at least rho. To prove this, write
the roots as lambda_i. The discriminant

    disc(p)=c^(2m-2) product_(i<j) (lambda_i-lambda_j)^2

is a nonzero integer: it is a polynomial with integer coefficients in
the coefficients of p, and squarefreeness makes it nonzero. Hence its
absolute value is at least 1. For any chosen pair of roots at distance d,
all N-1 other pair distances are at most 2R. Therefore

    1 <= c^(2m-2) d^2 (2R)^(2N-2),

which gives d>=rho. All roots are real because the pencil is definite;
the same estimate with complex root moduli would also suffice algebraically.

This intentionally crude bound is explicit, computable, and fully rigorous.
It can be much smaller than the true separation. Exact squarefree Sturm
counts in the cluster can be far cheaper or sharper than requiring w<rho.
The current low_band.py already has that exact root-count route; this note
does not claim the new discriminant route is implemented.

### Ground-rank inference theorem

Under Section 1 and the arithmetic assumptions above, if

    w < rho,

then all r energies in the cluster coincide. Otherwise two distinct roots
in [a,b) would be separated by less than w<rho, a contradiction. Therefore

    g=r,   Delta >= gamma.

No ground rank was assumed. It is a proved output. Independently, m>=2
implies Delta>=rho for this finite matrix, even if the cluster fails to
collapse. The latter bound is often quantitatively useless but is a true
gap bound that does not require knowing g.

If a narrower cluster enclosing precisely the lowest eigenspace is sought,
exact inertia/Sturm refinement at fixed finite H eventually resolves it.
This need not involve computing numerical eigenvalues. It may still cost
exponentially in physical size. If one insists on retaining the original
r when it includes distinct energies, its width cannot be driven to zero:
every valid enclosure has width at least E_(r-1)-E_0>0. The algorithm must
split the cluster, not reinterpret it as a degenerate ground space.

## 4. A thermal criterion that infers multiplicity

A known positive distinct-root bound rho also converts a purity interval
into a rigorous multiplicity test. It is legitimate for rho to come from
Section 3, or from a separately proved structural spectral separation.
Let m>=2, and suppose certified trace bounds give

    T^- <= T(beta) <= T^+.

For the true unknown g, shift E_0 to zero and write
S=sum_(excited a) exp(-beta(E_a-E_0)). Then

    S <= (D-g) exp(-beta rho),
    T(beta) <= 1/g,
    T(beta) >= g/(g+S)^2.

The upper bound follows because every Gibbs probability is at most
1/(g+S)<=1/g. The lower bound retains only the g ground weights in the
purity numerator. In particular

    0 <= 1/g-T(beta) <= 2 S/g^2
                           <= 2(D-1) exp(-beta rho) = B.

Here 1-(1+x)^(-2)<=2x for x>=0 was used. Consequently retain only integer
candidates k in {1,...,D-1} satisfying

    1/k in [T^-, T^+ + B].

The actual g is always retained. If exactly one candidate remains, it
certifies g without prior input. One may restrict k<=r if Section 1 is
available, or use the sharper k-dependent bound above. If none remains,
the supplied certificates are inconsistent; that is not a new physical
conclusion. If several remain, multiplicity is unresolved.

For fixed finite D,rho and arbitrarily accurate trace enclosures, the
criterion eventually isolates g as beta increases: B tends to zero and
the finite candidate set has positive spacing. This is an existence and
verification statement, not an efficient algorithm or a spatial bootstrap.
No exact ground energy is required as input: the shift by E_0 above is
only a proof device, and T=Z(2 beta)/Z(beta)^2 is energy-shift invariant.
The finite-beta candidate test needs a separately certified rho and D,
not access to beta=infinity. Its existence guarantee as precision and
beta increase is separate from any finite computational budget.
Once g is inferred, the finite temporal formulas in DEGENERATE_PURITY.md
apply with an evidentially justified g.

There is also a purely asymptotic characterization. For a fixed matrix
with first excited energy Delta and its multiplicity h,

    1/g-T(beta) = (2h/g^2) exp(-beta Delta)
                 + o(exp(-beta Delta)).

This follows by writing S=h exp(-beta Delta)+o(exp(-beta Delta)),
Q=sum exp(-2 beta(E_a-E_0))=O(exp(-2 beta Delta)), and
T=(g+Q)/(g+S)^2. Thus a proved estimate

    0 <= c-T(beta) <= C exp(-beta delta)

for unbounded beta, with c=lim T(beta), implies Delta>=delta and
c=1/g. It does not require g as an initial assumption. Merely fitting
an exponential or observing several temperature doublings does not prove
this all-temperature hypothesis. An actual recurrence establishing this
limit and rate is the missing theorem in any proposed thermal bootstrap.

## 5. What is and is not uniform in volume

A family theorem must use one specified Hamiltonian family and prove its
hypotheses for every covered volume L. Two useful sufficient conditions are:

1. Each volume has a counted bottom cluster, an arithmetic separation rho_L,
   and w_L<rho_L, while gamma_L>=gamma_*>0. Then g_L=r_L is inferred at
   every volume, and Delta_L>=gamma_*. The ranks may vary with L.
2. A structural proof gives every distinct-energy spacing at least rho_*>0
   uniformly in L. Then the true gap is uniformly at least rho_* whenever
   excited states exist, regardless of g_L. This is a very strong spectral
   statement, not a consequence of rational entries or finite locality.

Neither w_L->0 nor gamma_L>=gamma_*>0 alone satisfies either condition.
The rational family diag(0,2^(-L),1) has w_L=2^(1-L)->0 and gamma_L->1
using the brackets in Section 2, yet Delta_L=2^(-L)->0. This is a finite
matrix-family counterexample, not a claimed fixed-coupling local lattice
model. It suffices to refute an inference based only on these spectral
certificates. Any rescue from locality needs an additional proved theorem.

Arithmetic bounds have no automatic positive volume-uniform infimum.
The degree m_L can grow as the Hilbert dimension, coefficient heights and
cleared denominators can grow, and the exponent N_L is quadratic in m_L.
Even bounded local rational couplings therefore do not make the displayed
rho_L uniform. A width contracting exponentially in linear size need not
outrun this much smaller arithmetic scale. One must compare the actual
proved bounds, not merely note that both sequences tend to zero.

Finally, knowing or inferring g_L still does not repair the old spatial
purity bootstrap. Scaling the temporal edge by g_L changes its mixed
exchange factors; scaling all edges does not make the spatial ratios
trace purities. The exact Ising example in DEGENERATE_PURITY.md proves
this failure. A valid unknown-rank spatial theorem must independently
establish its spectral/transfer structure, compatible edge identities,
rank inference or band notion, contraction, and all-integer interpolation.

## 6. Recommended certificate outputs

Report the bottom-cluster rank r, width bound w, and external separation
gamma as established quantities. Leave ground rank and true ground gap
unresolved unless an additional proof is supplied. Acceptable additional
proofs include a single distinct-root count, w<rho with an audited
separation witness, an applicable multiplicity theorem forcing g=r, or
the uniquely surviving thermal candidate in Section 4.

For finite rational matrices, rho is also an independent true-gap fallback.
Label it finite-volume and keep its potentially tiny value explicit.
A uniform-family claim requires the corresponding all-volume inequalities,
not extrapolation from a finite set of successful examples.

## 7. Resource limits and a quantitative thermal precision target

The characteristic-polynomial/Sturm construction avoids calculating or
storing the full numerical eigenspectrum. It nevertheless requires the
full finite operator, a complete collection of invariant blocks, or an
independently proved symbolic characteristic polynomial. A polynomial
computed only in an unverified trial subspace does not supply a full-space
root separation bound. Exact factorization, polynomial coefficient heights,
and full-space inertia can dominate the cost. This is not a general
low-rank-only scalable solution.

For a concrete sufficient precision budget, the separation between different
reciprocals in {1,1/2,...,1/D} is at least eta=1/[D(D-1)] for D>=2.
If the purity interval has width at most eta/4 and

    beta >= rho^(-1) log[8(D-1)/eta],

then B<=eta/4, so the candidate interval has width at most eta/2 and
contains exactly one candidate. The proof already ensures it contains the
true g. This is a sufficient, conservative resource target, not a necessary
one. A known r can reduce the candidate set, but the omitted-state bound
still has to cover the full complement. The dependence on rho^(-1) is often
prohibitive; the discriminant estimate can make it much worse than any
practical cooling scale. Trace-enclosure cost at that temperature remains
an independent obligation, especially when energy uncertainties are
multiplied by beta.

Partial-spectrum methods become economical only when a separate structural
inequality bounds the omitted states or infers multiplicity without these
full-degree polynomial operations. The cluster certificate of Section 2
provides one valid partial-information output even when such stronger
structure is unavailable. It must retain its band interpretation.
