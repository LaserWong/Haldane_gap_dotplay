# Derivations and certificate scopes

## 1. Scalar basin and the invariant failure region

Write spatial and thermal purity lower bounds as S,T and define

G(x)=1−(1−x)^2/(2x^2).

The original sequential update is S'=G(S²T), T'=G(T²S'). G is increasing on (0,1], and

G(x)−x=(1−x)(2x−1)(x+1)/(2x²).

Hence G(x)≤x for x≤1/2. If W=S²T≤1/2, either a bound becomes nonpositive immediately, or S'≤W≤S and T'≤T²S'≤T. Both purities decrease and W cannot leave this region. Consequently W≤1/2 cannot reach a small-defect contracting region for this scheme. This is an impossibility for the scalar method with those exact purities, not a statement about the physical gap.

The same argument applies to the cyclic three-purity map whose first argument is A⁴B²C. If it is at most 1/2, the subsequent pre-update arguments are at most the preceding updated purity, so all three decrease over a full cycle.

The basin-boundary code uses DOWNWARD trajectories to prove acceptance and UPWARD trajectories to prove exclusion. Failure of a downward bound alone is never an exclusion proof. Monotonicity makes accepted and excluded endpoints valid boundary brackets.

## 2. A larger one-dimensional entry region

For p,q≤u, the exact spatial coefficient is

p'/u²≤(3−3u+u²)²/[2(1−u)^6].

The inner ratio (3−3u+u²)/(1−u)^3 has derivative with positive numerator 6−4u+u². Thus the coefficient is increasing, and at u=1/40 it is 4.981724…<5. The subsequent thermal update is bounded by

q'/u²≤(2+5u)^2/[2(1−(2+5u)u)^2]<5

on the same interval. The original all-integer interpolation checks still hold at u=1/40:

3/2+5u+2/(1−2u)<4, and 4/(1−4u)<5.

The dominant-transfer-weight argument only needs u<1/8. Therefore u_j≤(5u_0)^(2^j)/5 and the original all-integer gap bound log(1/(5u_0))/beta_0 hold for u_0≤1/40.

## 3. Exact n=2 uniform Heisenberg exclusion

For periodic length two retain both bonds: H2=2 S1·S2. Its total-spin J levels are

E_J=J(J+1)−2s(s+1), multiplicity 2J+1.

For length four,

H4=(S1+S3)·(S2+S4).

Let a,b=0,…,2s denote the sublattice pair spins. For each a,b, J=|a−b|,…,a+b occurs once, with energy [J(J+1)−a(a+1)−b(b+1)]/2 and multiplicity 2J+1. The ground energies are E0(2)=−2s(s+1), E0(4)=−2s(2s+1), so C2=2s exactly.

Put t=2s and x=exp(−2 beta). Let Q2(x)=sum_J (2J+1)x^[J(J+1)/2], and let Q4(x) collect the exact length-four excitation energies. Then

W(beta)=x^t Q4(x)/Q2(x)^4.

For rational U, positivity of P(x)=U Q2(x)^4−x^t Q4(x) on [0,1] proves W≤U for every beta≥0. A degree-d polynomial with power coefficients a_i has Bernstein coefficients b_k=sum_(i≤k) a_i binom(k,i)/binom(d,i). Since each Bernstein basis function is nonnegative, nonnegative b_k prove positivity. Repeated rational de Casteljau bisection proves positivity on the few reported subintervals. This is an exact finite certificate, with no diagonalization and no temperature-grid assumption.

## 4. Counted spectral bins, derivatives, and necessary temperature windows

For each certified spectrum, a unique ground enclosure and bins containing exact eigenvalue counts give lower/upper excitation gaps. Every trace term is monotone in beta and in its gap, yielding rational interval bounds on Q(beta)=1+R(beta). For a beta interval [a,b], x exp(−beta x) is bounded by its endpoint values and, for the upper bound, its sole interior maximum x=1/beta. This bounds energy expectations and hence

d log W/d beta=−2 C_n−2<excitation energy>_(2n,2beta)+4<excitation energy>_(n,beta).

Derivative envelopes can certify monotonic intervals or bound between-grid variation. If C_n has a positive lower bound, W≤D_(2n) exp(−2 beta C_n^−) handles the infinite beta tail exactly.

A simpler necessary-overlap test uses two certified scalar failure coordinates: (S,T)=(3/4,1) and (1,79/100) are both excluded by upward replay. Thus success requires S>3/4 and T>79/100. Counted low levels imply

T≤p_ground≤1/[1+sum_low c_j exp(−beta Delta_j^+)].

This gives a necessary lower-beta cutoff. Conversely,

S≤exp(−beta C_n^−) Q_(2n)^+(beta)

is decreasing and supplies a necessary upper-beta cutoff. If the lower cutoff exceeds the upper cutoff, that n is rigorously excluded. It is not a failure statement about the numerical moment order m.

## 5. Two-color dimer heat-trace improvement

Consider the report's disjoint-cell perturbations v_i on an even cycle of M cells. Center them by their maximally mixed cell mean. The v_i mutually commute because cells are disjoint; their joint spectral projectors and the unperturbed product-dimer Gibbs state define an ordinary joint probability law. Even cells touch mutually disjoint strong dimers, as do odd cells. Within either color, the selected cell marginal factorizes into maximally mixed cell states.

Cauchy–Schwarz between the two color sums gives

E exp(−beta sum_i v_i)≤[E exp(−2beta sum_even v_i) E exp(−2beta sum_odd v_i)]^(1/2).

Each color's expectation factorizes. Hoeffding's lemma for a mean-zero variable of range width w gives exp((2beta w)^2/8) per cell. Thus

0≤log Z_M−log Z_M^0≤M beta² w²/4.

This improves the prior M² bound. Golden–Thompson supplies the upper quantum-to-classical reduction; no commutation between H0 and V is assumed. This coloring shortcut does NOT automatically apply to overlapping bilayer interaction terms, which need their separate local relative comparison.

Primary sources for the general inequalities: W. Hoeffding, JASA 58 (1963), 13–30, https://doi.org/10.1080/01621459.1963.10500830; S. Janson, Random Structures & Algorithms 24 (2004), 234–248, https://doi.org/10.1002/rsa.20008 and author's full paper https://www2.math.uu.se/~svantejs/papers/sj150.pdf. The two-color application above is proved explicitly, rather than imported as a black box.

## 6. Cancel correlated traces before interval arithmetic

In 1D, W=S²T=Z_(2n)(2beta)/Z_n(beta)^4. Evaluating this cancelled ratio directly avoids applying the error of the common Z_(2n)(beta) twice. Set S1=G(W_lower), then T1=G(T_lower² S1); continue at doubled n,beta. This uses no new input partition functions.

In 2D, for the x,y,time staircase,

A=Z42(beta)/Z22(beta)², B=Z44(beta)/Z42(beta)², C=Z44(2beta)/Z44(beta)².

The first two needed combinations are

J1=A⁴B²C=Z44(2beta)/Z22(beta)^8,
J2=B⁴C²=Z44(2beta)^2/Z42(beta)^8.

Use A1=G(J1_lower), B1=G(J2_lower A1), C1=G(C_lower⁴ A1² B1), then continue at doubled sizes/temperature. If Z=e^(−beta U)Q uses certified ground-upper pivot U, numerator Q≥1 and denominator Q≤Q_upper provide the required lower ratios. All energy-shift factors are combined before exponentiation.

## 7. Legitimate axis orders

For any permutation of x,y,time, rebuild the staircase of partition functions from its base point; do not merely permute three preexisting bounds. The coordinate-independent exchange identity and own-axis squaring yield the same cyclic map. To convert an accepted staircase to the canonical x,y,time interpolation theorem, an adjacent pair (a,b) may be swapped with bounds (a sqrt(b), a²b), or the weaker rational-only pair (ab,a²b). At most three adjacent swaps suffice. The implementation uses the weaker pair and continues iterations until the converted common defect is at most 1/500.

This preserves the documented square-gap formula log(1/(32u))/beta. The resulting theorem starts at the reported L0. Missing smaller square sizes need independent certificates; a stronger asymptotic number is not a full all-L improvement unless that bridge is proved.

## 8. Rigorous ceiling of the current half-spin bilayer majorants

For the exact local comparison from `root_review/BILAYER_LOCAL_ANALYTIC.md`,

b(a)=sqrt(a²−ag+g²)−a+g/2, a≥g/2,
alpha=1−4a, B=2N b(a).

Its first-bin optimum is

max_a(alpha−B)=1−2g−2g sqrt(3(N−1)).

Even if the unconstrained optimizer falls outside a<1/4, this expression remains an upper bound on the restricted optimum. The implemented upper tail has the binomial expansion

exp[beta(B+U−E00)] ((1+3 exp(−beta alpha))^N−1).

Its first term proves that EVERY allowed choice of a gives Q_upper at least

1+3N exp(−beta delta_best),
delta_best=1−2g−2g sqrt(3(N−1))+E00−U.

Thus this expression gives an optimistic upper envelope on the lower purity bounds that the recipe can produce. It is NOT an upper bound on the true physical purity. To permit all future ground refinements, maximize delta_best by allowing U to fall as low as the currently certified ground lower endpoint. In energy-shift exponents, use the favorable endpoint independently for each coefficient sign. Also set the ground-enclosure width to zero. These changes can only make the optimistic envelope easier to pass.

The code encloses that optimistic envelope on every beta interval and propagates it UPWARD through the cancelled first update and cyclic scalar map. Reaching the invariant failure region proves impossibility for the whole interval. A positive lower corner curvature makes J1≤exp(−beta curvature), closing beta≥B. For g=.03 all three inequivalent axis orders are excluded with only 3–4 finite intervals plus the tail. Consequently ground-state digits alone cannot rescue this declared recipe at those sizes. Improved numerator levels, tighter excitation bins, a new comparison, larger/different seed geometry, or a different bootstrap method remain open.
