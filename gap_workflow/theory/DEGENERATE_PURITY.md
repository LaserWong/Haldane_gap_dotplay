# Ground-space-aware temporal purity and the Ising cycle certificate

## Result and boundary of the claim

Known exact finite ground multiplicity g permits a rigorous temporal
purity defect and a conservative quadratic temperature-doubling bound.
It does **not** permit substituting gT into the existing spatial bootstrap.
An explicit three-level spectrum even refutes keeping that bootstrap's
unique-state temporal recurrence, or merely multiplying its bound by g.

For the uniform ferromagnetic Ising cycle there is a stronger, separate
all-size certificate: the exact 2-by-2 transfer matrix identifies a
twofold ground space and gap J for every integer L >= 2. The spin-flip
sector reduction explains the scaled temporal purity, but fails the
spatial trace hypothesis needed by the old bootstrap. This supplies an
actionable alternative criterion rather than a larger seed search.

This note proves finite-matrix statements and one specified classical
family theorem. It does not establish a generic degenerate-ground-space
spatial bootstrap, a nearly degenerate band theorem, or a new Haldane gap.

## 1. Exact finite-matrix evolution

Let H be a finite Hermitian matrix with exactly g eigenvalues equal to
E0, and every remaining eigenvalue strictly greater than E0. For beta>0,
list excited eigenvalues with their actual multiplicities and write

x_a = exp[-beta(E_a-E0)],   0 < x_a < 1,
S = sum_a x_a,   Q = sum_a x_a^2,   R = sum_a x_a^4.

No excited multiplicity need be divisible by g. The shifted partition
function is g+S. Define the scaled temporal purity and its defect by

P_g(beta) = g Z(2 beta)/Z(beta)^2 = g(g+Q)/(g+S)^2,
u(beta) = 1-P_g(beta)
        = (2gS + S^2 - gQ)/(g+S)^2.                         (1)

Every Gibbs probability is at most p0=1/(g+S); hence T<=p0<=1/g,
0<=P_g<=1, and P_g tends to 1 as beta tends to infinity. If there are
excited states the finite-temperature inequalities P_g<1 and u>0 are
strict. If g equals the whole Hilbert dimension, u=0 and no excitation
gap should be reported.

At the doubled inverse temperature, the exact evolution is

u(2 beta) = (2gQ + Q^2 - gR)/(g+Q)^2.                    (2)

Thus u alone does not determine the exact next value. Equations (1)-(2)
retain the moments needed for exact replay. They are energy-shift
invariant. Certified trace intervals give P_g >= g Z^-(2 beta)/Z^+(beta)^2
only once the chosen g has been justified for this Hamiltonian.

A safe one-variable upper bound follows as follows. Since T<=p0,

1-u = gT <= g/(g+S),   so S <= g u/(1-u).               (3)

Also Q<=S^2, and

u(2 beta) <= 1 - [g/(g+Q)]^2 <= 2Q/g.

Consequently, for every 0<=u<1,

u(2 beta) <= 1-[1+g(u/(1-u))^2]^{-2}
           <= 2g [u/(1-u)]^2.                          (4)

The first bound can be useful when the second exceeds one. These are
conservative sufficient bounds, with no claim of optimal constants.
A direct finite-volume gap certificate follows from max_a x_a<=S:

Delta >= beta^{-1} log[(1-u)/(g u)],                    (5)

provided u<1/(g+1); a certified upper bound on u may replace u. This is
the gap above the full exactly g-dimensional ground space, not a
within-band splitting. Formula (5) needs at least one excited state.

For a fixed finite H, u<=1/2 makes (4) at most 8g u^2. Thus u0<1/(8g)
yields a temperature-only iterative bound

u_j <= (8g u0)^{2^j}/(8g),   beta_j=2^j beta0.

It certifies Delta >= beta0^{-1} log[1/(8g u0)] by (5) and the limit
j->infinity at fixed H. This does not propagate across volumes.

Ground multiplicity must be separately proved, including all omitted
sectors. A numerical cluster is insufficient. For a family, the theorem
must establish g_L for every covered volume; assuming a single g demands
proof that it is constant throughout that family. Sector crossings,
boundary modes, and exponentially small splittings cannot be silently
absorbed into an exactly degenerate ground space. If g is guessed too
large, P_g can exceed one and the defect ceases to be a purity defect.

## 2. Why the old scalar recurrence fails

Take the exact spectral fixture H=diag(0,0,Delta), with
exp(-beta Delta)=1/10 and g=2. The excited multiplicity is one. Equations
(1)-(2) give

u = 13/147,
u(2 beta) = 133/13467.

The unique-ground-state recurrence would bound the latter by

f(u) = u^2/[2(1-u)^2] = 169/35912.

In fact u(2 beta)>2 f(u)>f(u). Both the unmodified recurrence and the
simple g f(u) replacement are false. At small single-excitation weight
x one has u=2x/g+O(x^2) and u(2 beta)=2x^2/g+O(x^4), so the limiting
quadratic ratio is g/2. The finite-x corrections still matter.

There is a stronger special hypothesis under which f does hold:
H is unitarily equivalent to I_g tensor K, with K having a unique ground
state. Then Z_H=g Z_K and P_g is exactly the Gibbs purity of K.
All eigenvalue multiplicities, not only the ground multiplicity, must
support this identical-sector decomposition. A merely invariant sector,
or several sectors with differing excitation spectra, is insufficient.
Even this stronger temporal statement does not give K the requisite
spatial transfer structure.

## 3. Spatial normalization and exchange factors

For the physical partition function define P_i(v)=Z(D_i v)/Z(v)^2,
with commuting coordinate doublings. The unscaled exchange identity is

P_i(D_j v) P_j(v)^2 = P_j(D_i v) P_i(v)^2.

Suppose constants a_i are introduced in each direction, R_i=a_i P_i.
Then the exact identity becomes

R_i(D_j v) R_j(v)^2
  = (a_j/a_i) R_j(D_i v) R_i(v)^2.                      (6)

Scaling the temporal edge by g but leaving spatial edges unchanged
therefore changes mixed exchange factors. If the a_i vary with v, the
factor instead is

a_i(D_j v) a_j(v)^2 / [a_j(D_i v) a_i(v)^2].

Dividing every partition function by the same g scales **every** edge
by g and restores the formal exchange identity. It does not ensure
these scaled spatial edges lie in (0,1], or that they are trace purities.

For a fixed real selfadjoint transfer X and even powers L, if the largest
absolute eigenvalue has multiplicity m, then

Tr X^{2L}/(Tr X^L)^2 -> 1/m as L -> infinity through even L.

The spatial scaled ratio gP consequently tends to g/m. Physical ground
multiplicity g at beta=infinity says nothing sufficient about m at a
fixed positive beta. Leading negative eigenvalues and odd-length
interpolation add separate sign and multiplicity obligations. The old
interpolation proof assumes a unique dominant absolute eigenvalue and
cannot be copied to a degenerate dominant space without another proof.

Any prospective multi-direction degenerate theorem must specify actual
transfer multiplicities, compatible direction-dependent normalizations,
exchange factors, and all-integer interpolation. These are structural
proof obligations, not numerical flags or tail-truncation tolerances.

## 4. Exact Ising cycle family

Let

H_L = -J sum_(i=0)^(L-1) Sz_i Sz_(i+1 mod L),
J>0, Sz eigenvalues +/-1/2, L>=2.

The length-two member has two parallel bond occurrences. Let
b=beta J/4 and t=exp(-beta J/2). The physical transfer matrix is

V = [[exp(b), exp(-b)], [exp(-b), exp(b)]],
lambda_+ = exp(b)(1+t),   lambda_- = exp(b)(1-t).

Both eigenvalues are positive and lambda_+>lambda_- for finite beta>0.
The partition function is exactly

Z_L(beta) = Tr V^L
          = exp(beta JL/4) [(1+t)^L+(1-t)^L]
          = 2 exp(beta JL/4) A_L(t),
A_L(t) = sum_(k even) binomial(L,k) t^k.                 (7)

One direct proof is to record which cycle bonds are domain walls.
A periodic sign sequence has an even number k of walls; each even
subset of bonds determines precisely two configurations, related by
global spin flip. Each wall raises the energy by J/2. Hence the
coefficient identity is also a complete spectral counting proof,
including at L=2:

E0 = -JL/4,   ground multiplicity = 2,
Delta_L = J,  first excited multiplicity = 2 binomial(L,2),
for every integer L>=2.                                (8)

There are no powers t^1, and the coefficient at t^2 is nonzero for every
allowed L. This proves the **uniform family** gap directly from the
all-size transfer polynomial, not from finite numerical checks.

### Genuine two-sector decomposition, with its limitation

The global flip U pairs every computational configuration sigma with
-sigma. Symmetric and antisymmetric pair combinations span the two U
sectors. H is diagonal in these pair combinations with identical
sector spectra. Each sector has one ground state, and H is unitarily
I_2 tensor K_L. Thus Z_K=Z_L/2 and

P_2(beta) = A_L(t^2)/A_L(t)^2

is an actual unique-ground-state sector purity. In this special model
the old **temporal** defect map f is valid. The identical blocks prove
that the sector excitation gap is the full ground-space excitation gap;
this conclusion would be invalid for arbitrary unequal sectors.

However W_L=Z_L/2 does not obey the needed ordinary spatial trace
identity. In particular its spatial ratio is

W_(2L)/W_L^2 = 2 (1+r^(2L))/(1+r^L)^2,
r=lambda_-/lambda_+ in (0,1).

This is strictly greater than one because
2(1+y^2)-(1+y)^2=(1-y)^2>0 for y=r^L<1, and tends to two as L grows.
Consequently it cannot be the purity of a fixed selfadjoint spatial
transfer at even L. The prefactors 1/2 in
W_L=(lambda_+^L+lambda_-^L)/2 are not integer spectral multiplicities.
At finite beta the physical transfer has leading multiplicity m=1,
although the physical ground-space dimension is g=2. This is an exact
counterexample to equating those multiplicities.

For context, (7) also gives a useful uniform tail estimate. With
x=L exp(-beta J/2),

A_L(t)-1 <= cosh(x)-1,
1-P_2 <= 1-A_L(t)^(-2) <= 2[cosh(x)-1] <= x^2 cosh(x).

Here binomial(L,k)<=L^k/k!, and the last inequality follows coefficient
by coefficient in the power series. It explains cooling requirements
without a Hilbert-space enumeration. It is not used to assert an
unproved mixed spatial recurrence.

## 5. Actionable criterion and verification

For a detected exact Ising cycle family, route to the coefficient/
domain-wall certificate (7)-(8), record the twofold full ground space,
and stop trying to enter a unique-full-ground-state purity threshold.
For a different degenerate family, first prove its exact ground rank,
then choose a full-space spectral/comparison or ground-space-aware
finite-size criterion. Scaled temporal purity can certify a finite
volume via (5); it alone cannot certify an arbitrary uniform family.
Only attempt a new spatial bootstrap after the obligations in Section 3
have been discharged analytically.

`gapflow/degenerate.py` implements exact-rational fixture diagnostics,
the cycle pair-counting polynomial, and a theorem report for the
specifically defined uniform cycle family. It deliberately does not
register a new generic bootstrap adapter, infer a physical g, or claim
that an arbitrary input model belongs to the cycle family.

`tests/test_degenerate.py` checks the non-divisible-multiplicity
counterexample exactly; 120 rational finite spectra; repeated identical
sectors; full configuration counts for L=2,...,10; transfer polynomial
identities at rational t; the invalid spatial normalization; and input
validation. These tests support implementation correctness, while the
all-size assertions are proved above.

Run: `python -m unittest discover -s tests -p test_degenerate.py -v`.
All eight test methods passed on 14 October 2026 (including the causal controls below). No remote publication,
new installation, or uncontrolled diagonalization is needed.

## 6. Causal controls: degeneracy, physical U(1), and sector restriction

The obstructing statement is precise: a full Gibbs state with g>=2 has
T<=1/g, so it cannot meet a near-one unique-ground-state seed condition.
This is caused by exact ground degeneracy. It is not a consequence of
absence of the physical U(1) generated by total Sz. In fact the Ising
counterexample has that U(1). Here U(1) always means this specified
physical spin rotation, not an arbitrary continuous group generated by
some conserved spectral projector.

### Controlled comparison table

| Control | Physical U(1): [H,Mz]=0? | Ground-space fact | Seed implication and exact failure source | Evidence |
|---|---|---|---|---|
| Ferromagnetic zero-field Ising cycle | Yes | g=2; gap J | Full temporal purity <=1/2, so unique-ground-state entry is impossible | Analytic all-L proof, Sections 1 and 4; ISING_OBSTRUCTION.md |
| Same cycle plus longitudinal field -h sum Sz, h>0 | Yes | g=1; gap min(Lh,J+h) | The degeneracy obstruction disappears; fixed staircase purities approach one as beta grows | Analytic energy and transfer proof below; finite rational spectrum checks |
| Graph-state projector Hamiltonian | No | g=1; gap h | No physical-U(1) obstruction: scalar spatial transfer and a certified near-one seed are available | Analytic unitary spectrum and transfer proof in STABILIZER_BENCHMARK.md; commutator proof below |
| One global-flip sector of zero-field Ising | Mz does not preserve this sector | One ground state in each of two identical sectors | Temporal purity is valid, but its spatial ratio exceeds one; ordinary transfer-trace hypothesis fails | Exact sector and spatial-ratio calculation in Section 4 |

These examples distinguish a falsified necessary premise from a merely
unproved hypothesis. The first is a proved all-temperature upper-bound
obstruction. The fourth is a proved failure of the proposed normalized
spatial purity. Neither is evidence of physical gaplessness. The second
and third are controlled counterexamples to attributing failure to the
presence or absence of physical U(1).

### Explicit operators and symmetries

Use X,Y,Z for Pauli matrices and Sz=Z/2. Write

Mz = (1/2) sum_i Z_i,
U_flip = product_i X_i,
H0 = -(J/4) sum_i Z_i Z_(i+1).

Every term of H0 is diagonal in the Z basis, so [H0,Mz]=0. This proves
invariance under exp(i theta Mz) for every real theta. Also
U_flip Z_i U_flip^*=-Z_i, hence [H0,U_flip]=0. Positive ferromagnetic
couplings on a connected cycle make the only wall-free configurations
all-up and all-down. Their common energy is minimal, giving exactly two
ground states. Both positivity/connectedness and the explicit spectrum
matter: a Z2 symmetry by itself does not force a degenerate ground
state, and neither does U(1).

Add the longitudinal field Hh=H0-h Mz, with h>0. Then [Hh,Mz]=0 still,
whereas U_flip Hh U_flip^*=H0+h Mz differs from Hh. Relative to all-up,
a configuration with down-spin set S and k domain walls has

E_h(S)-E_h(empty) = J k/2 + h |S|.

This is strictly positive for every nonempty S. The all-down state has
cost hL. Every nonempty proper S has k>=2 and |S|>=1, so its cost is at
least J+h; a single down spin attains this value. Therefore the full
finite-volume ground is unique and its exact gap is min(hL,J+h),
including L=2 with its two bond occurrences. The uniform lower bound
min(2h,J+h)>0 holds for all L>=2.

This longitudinal-field family also retains an exact real symmetric
transfer matrix. With sigma,tau in {+1,-1}, set

V_h(sigma,tau) = exp[beta J sigma tau/4
                         + beta h(sigma+tau)/4].

Multiplying around a cycle counts every bond and field exactly once,
so Z_L=Tr V_h^L. Its determinant is exp(beta J/2)-exp(-beta J/2)>0 and
its trace is positive, so both eigenvalues are positive. Its exact
ground energy is E0(L)=-L(J/4+h/2), which is additive under doubling.
For every fixed finite staircase, ground uniqueness therefore gives
all spatial and temporal purity ratios tending to one as beta tends
to infinity. Thus sufficiently cold exact seeds exist for this
specified family; this is an existence statement, not an optimized
finite-temperature numerical certificate. Holding the physical U(1)
fixed while breaking the flip symmetry removes the obstruction.

For the graph-state control, take any finite simple graph and

K_i=X_i product_(j adjacent i) Z_j,
H_G=(h/2) sum_i (I-K_i),   h>0.

Since only Z_i in Mz fails to commute with K_i,

[H_G,Mz] = (i h/2) sum_i Y_i product_(j adjacent i) Z_j != 0.

The Pauli strings have distinct locations of Y and are linearly
independent, so they cannot cancel. Thus the physical U(1) is absent.
Nevertheless controlled-Z conjugation makes H_G a sum of independent
X-projectors; its ground is unique and gap is h. The rectangular family
has Z=(1+exp(-beta h))^N and the positive scalar spatial transfer
established in STABILIZER_BENCHMARK.md. It supplies an exact successful
purity benchmark without physical U(1). These commuting many-body
stabilizers are not being relabeled as a generic two-body or
noncommuting model.

Finally, U_flip Mz U_flip^*=-Mz. Mz maps the + and - flip sectors into
each other rather than defining a conserved physical-U(1) action
within one chosen flip sector. Restricting to a fixed magnetization
sector is a different operation and must not be conflated with fixing
global spin-flip parity. Neither restriction alone establishes a full
system gap. In this Ising example the identical flip-sector spectra
supply that extra gap argument, but still do not repair the spatial
normalization failure.

### Evidence and source accounting

All causal claims above follow from displayed operator identities,
exact energy differences, or finite-dimensional transfer formulas.
No external numerical observation is being used as their premise.
`tests/test_degenerate.py` adds exact rational longitudinal-field
spectral checks and explicit computational-basis commutator checks.
They check conventions and implementation, not the all-L proof.

For every failed candidate, the report should identify the failed
condition and its evidence: exact ground multiplicity versus the
near-one threshold; incomplete full-space sector coverage; incorrect
spatial transfer normalization; or merely missing transfer proof.
Failure to certify a sufficient seed without one of these analytic
exclusions remains inconclusive and is not itself a counterexample.
