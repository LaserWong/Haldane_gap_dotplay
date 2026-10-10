# A posteriori trial-rank, search-space and numerical-seed criteria

Updated 2026-10-10 14:16 America/New_York / 18:16 UTC.

This document derives the tests used in this directory. They are **sufficient
certificate tests and explicitly scoped impossibility tests**, not universal
lower bounds on variational dimension, perturbation strength, or physical gaps.
All numerical examples use saved rational data. No new physical eigensolve,
large contraction, remote write, or modification of an input certificate occurs.

The ordinary model has spin-1/2 rungs with coupling one, two straight intralayer
couplings g, no crossed couplings, and positive-direction periodic multiedges.
The separate FF model has crossed coupling J=3/10 and straight coupling J+epsilon.
Never identify these two models or their coupling ranges.

## 1. Four dimensions, and the question that each answers

Use the following distinct quantities:

1. D: full physical Hilbert dimension. N spin-1/2 rungs give D=4^N.
2. d: independent linear directions in a search/optimization space S. A ground
   Ritz calculation in d dimensions can return only one retained state.
3. k: physical eigenstates retained in the certified thermal band, counting
   exact spin and momentum multiplicities. In the one-triplet-band examples,
   k=1+3N, independently of how the ground vector was constructed.
4. s and s_H: configuration support of the representation and of its complete
   H-image. Neither is generally d or k. A symmetry sum can be one direction
   with thousands of configurations. No MPS representation is used here;
   an MPS bond dimension would be a fifth, different quantity.

For the audited g=.03 largest small seed, D=4^16=4,294,967,296, k=49, the
compressed ground search has d=11, its expanded support is 20,081, and its full
H-image support is 452,093. There are additionally two explicit odd-parity
search blocks, of configuration dimensions 3,936 and 3,376, with 16 retained
vectors each; the latter has spin-reversal multiplicity two. Thus “11 vectors”
describes the ground search, not the complete 49-state certificate or its total
computational storage. Translation-compressed larger candidates use one
29-dimensional ground search and 3N retained triplet modes.

There is no model-independent lower bound d>1: the exact ground eigenvector
itself spans a one-dimensional perfect ground trial space. Meaningful lower
bounds must specify the allowed representation/search space or certificate
ansatz. Merely tightening a ground residual also cannot certify omitted states.

## 2. Certified separation turns full residuals into width budgets

Let H be self-adjoint, Q have k orthonormal columns, T=Q*HQ, and R=HQ-QT.
Suppose full-space spectral information, not the trial eigensolver, proves

    lambda_1(H) >= L0,    lambda_(k+1)(H) >= a,
    T <= r I < a I,       R*R <= epsilon I.

Write delta=a-r>0. The min-max count gives exactly k eigenvalues below a.
The high-spectrum component X of Q satisfies H_+X-XT=R_+. Integrating
exp[-t(H_+-r)] R_+ exp[t(T-r)] from zero to infinity proves
||X|| <= sqrt(epsilon)/delta. Equality of the two projector misalignment
norms follows by the singular values of the overlap of their rank-k bases.
Consequently the compression to ran(Q)^perp obeys

    C >= b I,   b = a-(a-L0) min(1,epsilon/delta^2).                 (2.1)

When

    epsilon < delta^3/(a-L0),                                    (2.2)

we have b>r. Here a-L0>=delta, since T>=L0 I. Thus (2.2) also ensures
that the uncapped epsilon/delta^2 expression in (2.1) applies.

For t<b the Schur complement has lower bound

    T-t I - R*(C-t I)^(-1)R >= T-t I-epsilon/(b-t) I.

Counting its negative eigenvalues proves, for every ordered Ritz value theta_i,

    theta_i - epsilon/(b-r) <= lambda_i(H) <= theta_i.             (2.3)

For example, at t=theta_i-epsilon/(b-r), b-t>=b-r, and the right side is
at least T-theta_i I, with at most i-1 negative eigenvalues. A sharper endpoint
solves w_i(b-theta_i+w_i)=epsilon; the existing project code instead checks
the full matrix Schur polynomial and can be substantially sharper still.

A convenient rational residual target guaranteeing all widths at most omega is

    epsilon <= omega delta^3 / [delta^2+omega(a-L0)],             (2.4)

together with strict separation. This is obtained by substituting (2.1) into
epsilon/(b-r)<=omega. The inequality is sufficient, not necessary. If Ritz
values themselves are only enclosed to width nu_i, add nu_i to (2.3).
Invariant sectors can use their own L0, r and residual bounds; doing so avoids
charging a large excited-state residual to a very accurate ground state.

### Full rational moments are the required data

For nonorthonormal rational columns W in physical metric J, store

    G=W*JW,   A=W*JHW,   B=(HW)*J(HW).

G must be positive definite, and B must use **every** reached output, not the
square of a projected matrix. The exact residual Gram is
Gamma=B-AG^(-1)A. Alternatively any rational coefficient matrix D gives

    E=B-AD-D*A+D*GD >= Gamma.

The exact PSD test epsilon G-E>=0 establishes the operator residual bound.
Small diagonal residuals alone do not establish the same epsilon for the whole
band: correlated residual columns can have a much larger operator norm.

## 3. Spectral-bin entropy specifies how much band information to retain

Suppose certified ordered lower bins partition all omitted eigenvalue indices.
For bin j let its multiplicity be m_j and its lower endpoint be a_j. Let
[l_i,u_i], i<=k, enclose a complete retained low band, including multiplicities.
Take s=u_1 and define

    L(beta) = sum_(i<=k) exp[-beta(u_i-s)],
    U(beta) = sum_(i<=k) exp[-beta(l_i-s)] + T_k(beta),
    T_k(beta) = sum_(omitted bins j) m_j exp[-beta(a_j-s)].        (3.1)

Then L<=exp(beta s)Tr exp(-beta H)<=U. Let w_i=u_i-l_i. The exact
relative trace uncertainty separates into two sources:

    U/L - 1 = W_beta + T_k/L,
    W_beta = sum_i exp[-beta(u_i-s)](exp(beta w_i)-1)/L.           (3.2)

This weighted width cost is often far better than exp(beta max_i w_i)-1:
excited-state uncertainty is Boltzmann suppressed, whereas ground width is not.
Given an allowed relative error eta, the practical acceptance test is

    W_beta + T_k/L <= eta.                                      (3.3)

A coarser sufficient rule is exp(beta omega)-1+T_k/L<=eta for all w_i<=omega.
Combine this rule with (2.4) to turn a thermal error budget into a residual
stopping criterion for growing the search space. Actual state/sector-specific
widths should be used whenever available.

For rung triplet-number bins, m_q=C(N,q)3^q. Keeping all bins below q_* requires

    k(q_*) = sum_(q<q_*) C(N,q)3^q,                             (3.4)

and the remaining entropy is exactly the positive sum in (3.1). Thus q_*=2
means k=1+3N, while q_*=3 gives k=1+3N+9 C(N,2): 49 versus 1,129 at N=16,
or 193 versus 18,337 at N=64. This count concerns physical states, not a
symmetry-compressed ground search dimension.

The diagnostic “entropy minus energy” of a bin is

    log(m_q)-beta(a_q-s).

No logarithms are needed in acceptance: evaluate the positive exponential sum
with directed rounding. A cruder sufficient threshold is
(D-k)exp[-beta(a_cut-s)]<=tau. If a_q>=alpha q-B, write x=3 exp(-beta alpha).
For q_* beyond the mode, r=x(N-q_*)/(q_*+1)<1 bounds all successive term ratios,
so

    T_k <= exp[beta(B+s)] C(N,q_*) x^q_* /(1-r).                 (3.5)

This derives directly from the binomial ratio and a geometric series.

### A legitimate minimum within a specified majorant

Fix beta, shift s, and the rule that every omitted one-triplet slot receives
its same available bin lower endpoint a_1. Keep the q>=2 tail unchanged.
If r of the 3N one-triplet slots are omitted, that chosen majorant is

    T(r)=T_(q>=2)+r exp[-beta(a_1-s)].                           (3.6)

For an absolute shifted-tail tolerance tau, the maximum permitted omitted
count is floor[(tau-T_(q>=2)) exp(beta(a_1-s))], clipped to [0,3N].
This is an exact minimum retained rank **for (3.6) and that tolerance**.
It is not a necessary thermal rank, lower bound on arbitrary trial vectors,
or a claim that partial-rank Schur completeness can be certified without
additional spectral information. Our posterior examples already possess the
complete-band enclosures before asking which information could be discarded.
`entropy_rank.py` proves the integer floor by separate lower and upper
exponential bounds; the two floors agree.

At beta=9.09 and tau=1e-4, g=.03 and .04 require all 13/25/49 band states in
this coarse-bin test on N=4/8/16. At tau=1e-3, g=.03 permits retained ranks
8/21/45. At g=.05,N=16 the q>=2 tail alone exceeds 1e-4: keeping all 49
one-band states cannot meet that particular tolerance. None of these arbitrary
tail tolerances alone decides bootstrap acceptance.

## 4. Exact startup budgets connect these errors to the spatial seed

Use three physical patches with rung counts N0,N1=2N0,N2=4N0 and energies
s_j including their constant shifts. Let L_j,U_j be (3.1), and H_j=U_j/L_j.
For the canonical spatial-spatial-temperature order define the hypothetical
zero-error truncated inputs

    j1_* = exp[beta(-2s_2+8s_0)] L_2(2beta)/L_0(beta)^8,
    j2_* = exp[beta(-4s_2+8s_1)] L_2(2beta)^2/L_1(beta)^8,
    c_*  = L_2(2beta)/L_2(beta)^2.

The actual rigorously certified lower inputs are

    J1 >= j1_*/H_0^8,  J2 >= j2_*/H_1^8,  C >= c_*/H_2^2.       (4.1)

The direct trace identities are J1=Z_2(2beta)/Z_0(beta)^8 and
J2=Z_2(2beta)^2/Z_1(beta)^8; they retain correlated energy cancellations.
The factors j1_*,j2_* include finite-size energy curvature. They need not
be near one merely because every residual and omitted tail is tiny.

Let G(x)=1-(1-x)^2/(2x^2), increasing on 0<x<=1. The canonical first cycle is

    A1=G(J1), B1=G(J2 A1), C1=G(C^4 A1^2 B1).                  (4.2)

Choose a positive target (A_*,B_*,C_*) whose exact subsequent cyclic replay
enters the already audited small-defect domain. Choose h_A,h_B,h_C in (0,1]
with G(h_A)>=A_*, G(h_B)>=B_*, G(h_C)>=C_*. For example the inverse is
1/[1+sqrt(2(1-p))], bounded upwards with a rational lower square-root bound.
The following three rational tests suffice:

    H_0^8 <= j1_*/h_A,
    H_1^8 <= j2_* A_*/h_B,
    H_2^8 <= c_*^4 A_*^2 B_*/h_C.                              (4.3)

Each follows by substitution in (4.2) and monotonicity. Thus their eighth roots,
minus one, are explicit permitted relative trace uncertainties. In computation
we avoid roots and test (4.3) exactly with outward enclosures of all inputs.

At g=.03,beta=9.09 choose target (.9706,.9567,.9870). Its exact replay enters
the 1/500 common-defect domain. Allowed relative trace excesses from (4.3) are
approximately 4.29856e-5, 4.21805e-5, 1.60904e-4. The actual conservative
excesses are 2.07615e-6, 1.26639e-5, 6.21465e-5, respectively. All exact
eighth-power tests pass. These are useful slack estimates rather than a new
claim about the optimized physical gap. The existing independently audited
small-seed certificate gives the uniform gap >.009195338283 for all square
integer sides L>=2 after its finite-size bridges.

A minimal *successful tested* numerical seed is the smallest geometry in an
explicit candidate catalog for which the full spectral/trace tests, startup,
recurrence and all needed finite-size bridges pass. It is only an upper bound
on what might suffice. A negative lower-bound replay is not an impossibility
test; the next sections give actual impossibility witnesses.

## 5. Genuine search-space obstruction from full second moments

Fix an allowed search space S with full matrices G,A,B and a permitted Rayleigh
interval I=[c-h,c+h]. If exact PSD proves

    B-2c A+c^2 G >= gamma G,                                  (5.1)

then every normalized psi in S satisfies ||(H-c)psi||>=sqrt(gamma).
For any t in I the triangle inequality gives

    ||(H-t)psi|| >= sqrt(gamma)-h.

Choose a rational alpha with alpha^2<=gamma and alpha>h. Consequently

    ||(H-t)psi||^2 >= (alpha-h)^2 for every t in I.              (5.2)

In particular t=<psi,Hpsi> gives a lower bound on the full residual of every
normalized trial whose Rayleigh quotient lies in I. If (alpha-h)^2 exceeds a
required residual target, no optimizer, rounding improvement, or alternative
coefficients *inside this fixed S* can meet the target. This does not exclude
a different one-dimensional or six-dimensional space containing better vectors.

`residual_obstruction.py` takes the full q2 corner of the saved 11D G,H,H2
moments. It never squares the q2 compressed Hamiltonian. Exact rational LDL
pivots prove (5.1); rational interval and square-root witnesses are saved.
The allowed interval runs from the saved ground lower endpoint to the saved
11D ground upper endpoint plus .001. It contains the saved 11D Rayleigh value.
The following are rounded displays of strict exact comparisons:

| g | Fixed q2 search dimension | Uniform residual² lower in I | Target | Saved 11D residual² |
|---|---:|---:|---:|---:|
| .02 | 6 | 3.21531525e-5 | 1e-6 | 4.58375234e-8 |
| .03 | 6 | 1.77756684e-4 | 1e-6 | 5.31536780e-7 |
| .04 | 6 | 5.75892653e-4 | 1e-5 | 3.03710787e-6 |
| .05 | 6 | 1.41043403e-3 | 1e-4 | 1.17679493e-5 |

Thus one-block enlargement resolves a genuine q2-ansatz accuracy obstruction.
It does not by itself resolve spatial-seed startup, as the next result shows.
These scalar deductions inherit the review status of the saved physical moments.

## 6. All-temperature exclusion of the specified smallest canonical staircase

This result uses **upper bounds on exact physical inputs**, not failed lower
certificate bounds and not merely failure to reach a sufficient basin.
For g=.04 and .05 take the fixed periodic ladder 2x2 -> 4x2 -> 4x4.
Its exact physical inputs obey 0<J1,J2,C<=1: spatial factors are purities of
even self-adjoint transfer powers and C is a Gibbs purity; J1 and J2 are
products of these spatial/thermal factors. If an upper bound exceeds one,
clipping it to one is therefore safe.

Consider only the deterministic canonical scheme (4.2), then cyclic updates
(A,B,C)->(B,C,G(A^4 B^2 C)), without later injecting new physical traces,
changing staircase order, or replacing the inequality. While all entries are
positive, every multiplication and G is monotone. Thus upper input enclosures
propagate to upper enclosures for the exact-input scheme. If a propagated upper
iterate is <=0, the exact-input scheme has already left its required positive
domain. Arbitrarily accurate or larger trial spaces cannot repair that same
exact-input recurrence. This is **not** a claim that the physical purity is
negative, that every method fails, or that the system is gapless.

### Hot interval: all 0<=beta<=4

For finite H, log C(beta)=log Z(2beta)-2log Z(beta) has derivative
2(<H>_beta-<H>_(2beta))>=0, because the derivative of <H>_beta is minus its
variance. Hence C(beta)<=C(4). The saved exact spectral bounds give
C(4)<.288 at each coupling. If A1 or B1 is already nonpositive there is failure.
Otherwise both are at most one and

    C1 <= G(C(4)^4) < 0.

The exact rational negative upper witness is saved.

### Middle interval: closed coverage [4,20]

Cover it by 320 closed boxes [b_l,b_h] of length 1/20. For any positive
exponential sum, choose each endpoint according to the sign of its exponent.
Let L_j(b_h) be a lower denominator bound and U_2(2[b_l,b_h]) the termwise
upper numerator bound. The exact ratios then satisfy

    J1 <= max_b exp[b(-2s2+8s0)] U_2(2[b_l,b_h])/L_0(b_h)^8,
    J2 <= max_b exp[b(-4s2+8s1)] U_2(2[b_l,b_h])^2/L_1(b_h)^8,
    C  <= U_2(2[b_l,b_h])/L_2(b_h)^2.

Every retained upper energy is >=s_j, so each L_j is nonincreasing; this
property is directly verified by the supplied spectrum data. Ground lower
endpoints can be below s_j, so their *upper* numerator terms use b_h; all
other terms select their correct sign endpoint independently.
For g=.04 every box has a nonpositive upper iterate by update 4. For g=.05
every box has one by update 2. All 640 boxes, inputs, failed update indices,
and negative witnesses are stored as exact rational numbers.

### Cold interval: all beta>=20

Let l2 be the physical ground lower endpoint of the largest patch and let

    d1=2l2-8s0>0,    d2=4l2-8s1>0.

Factor its numerator as e^(-2beta l2) V(2beta), where V is the positive sum
of retained and omitted lower-energy exponentials relative to l2. Every gap
in V is nonnegative. Denominator ground terms alone give

    J1 <= e^(-beta d1) V(2beta),
    J2 <= e^(-beta d2) V(2beta)^2,   C<=1.

Both right-hand sides decrease with beta. Their values at beta=20 already
force a nonpositive upper iterate by the second update for .04, and by the
first update for .05. This proves the entire half-line without a cutoff grid.

### Scope and provenance

The theorem is a new exact scalar deduction from six frozen full-band
certificate files, whose SHA-256 hashes are recorded. The g=.04/.05 physical
certificates were not independently reconstructed by this worker. A separate
review has now **passed** all six full physical-band reconstructions and the
all-beta scalar deduction: see `../small_seed_exclusion_review/physical_results.json`
and `../small_seed_exclusion_review/scalar_results.json`. The latter uses
independent 256-bit/70-term exponential arithmetic and checks every saved box,
the hot range and both cold rays. Original producer status fields and source
files are preserved; the separate review supplies their independent acceptance.
The globally proved failure-update bounds are four for .04 and three for .05;
the .05 middle/cold bounds are two/one, with three needed by the hot proof.
It excludes precisely this canonical small ladder even with exact physical
traces. It does not exclude other axis orders, intermediate geometries such as
3x3 -> 6x3 -> 6x6, a different transfer inequality, or a larger ladder.

## 7. How far a perturbation and how small a nonperturbative space?

For H(t)=H0+tV and fixed trial projection P=QQ*,

    ||R(t)|| <= ||R(t0)||+|t-t0| ||(I-P)VQ||,
    lambda_max(T(t)) <= r(t0)+|t-t0| ||Q*VQ||.

Together with separate whole-spectrum a(t),L0(t), these give explicit
separation and residual-width tests (2.2)-(2.4), followed by entropy/startup.
They are not a universal function of t: local interaction structure, spectral
separation, collective entropy and spatial curvature all enter. A crude
whole-volume bound ||V|| generally grows with volume and can be much weaker
than the local relative-form/number-sector comparisons used here.

Fixed rational trial vectors allow a particularly useful continuum test.
Their Rayleigh matrix is affine in t. Their full residual matrix for any
affine rational proposal D(t) is a quadratic matrix polynomial whose leading
coefficient is a positive Gram matrix. Thus it is Loewner convex: its value
inside a closed interval is <=the linear interpolation of its endpoint values.
A common epsilon G bound verified at both endpoints holds throughout. The
same applies to the scalar variance: its t² coefficient is Var_psi(V)>=0.
An affine local comparison PSD at both endpoints also holds throughout.
This explains why interval certificates can cover a continuum without sampling
interior points. Energy combinations must be formed *before* taking interval
maxima, to retain volume cancellations.

The nonperturbative FF reference is a direct counterexample to any claim that
small linear dimension is restricted to vanishingly small interactions:
its singlet product is an exact one-vector ground state for 0<=J<1/3,
with the separately proved rectangular-family uniform gap min(1,4-12J).
At J=.3, this is .4; this reference includes crossed exchanges.

The independent FF interval audit proves, on every square integer L>=2:

* One product trial direction per seed suffices throughout
  0<=epsilon<=.00475, with full nonzero perturbative residual included and
  uniform gap >.008090283176. The complete excited spectrum is still bounded.
* Optimized fixed sparse vectors, one retained ground state from search
  dimensions 23/93/377 on N=4/8/16, extend the closed continuum through
  epsilon=.00855, with uniform gap >.000768515509.
* Through epsilon=.0085 the stronger common bound is >.001703099464.

These are sufficient ranges, not maximal perturbations. The .00855 perturbation
is .855% of the unit rung coupling (2.85% of J=.3); the nonperturbative reference
coupling itself is .3. `examples.py` independently re-evaluates the saved
quadratic endpoint maxima, exact residual/separation corrections, and scalar
startup on all six new interval pieces. It relies on the independently audited
physical polynomials and whole-spectrum proof in `epsilon_interval_review/`.

## 8. Practical adaptive decision rule

For a proposed coupling, geometry and nested search family:

1. Obtain a whole-spectrum count/cutoff. If rank-k Ritz values do not fit below
   it, improve the comparison or represent the missing complete band; do not
   infer completeness from residuals. The archived .05 single-start solver
   missed two low modes and was correctly rejected.
2. Compute full G,A,B and certify matrix residuals. If width cost dominates
   (3.2), grow the *search* space. Test (5.1)-(5.2) to tell whether the current
   fixed space can possibly attain the required residual target.
3. If omitted-bin entropy dominates, increase the *retained physical band*,
   strengthen bin lower endpoints, or change beta. Use the positive-sum
   budget, not simply “k low eigenvalues look accurate.”
4. Test the exact startup budgets and recurrence. If near-zero trace error
   still fails only as a lower-bound computation, this is diagnostic. If the
   exact-input upper recurrence exits positivity as in Section 6, the specified
   seed/order is excluded; change geometry, order or method instead of buying
   more ground digits or more vectors on that same ladder.
5. Retain full finite-size bridges and the audited transfer hypotheses before
   promoting a numerical seed to an all-size gap theorem. The asymptotic
   entry side (e.g. 128 or 256) is not the largest numerically diagonalized seed.

## 9. Reproduction and limits

`REPRODUCE.sh` runs all four self-contained scalar/moment test programs with
one CPU/BLAS thread and a 1 GiB address-space ceiling. The largest measured
run, the all-beta interval proof, used about 75 MiB and 20 seconds. There are
no external theorem dependencies beyond the already specified project
spectral/transfer inputs; the new arguments are derived above. Numerical
rank, PSD, square-root and exponential acceptance use rational arithmetic.
Displayed decimals are explanatory only.

The source tree has no .git metadata. The root README's source-commit label
could not be independently verified; inputs are identified by hashes instead.
All changes from this task are confined to this new directory. The root README
and existing scientific records were left unchanged for parent integration.
