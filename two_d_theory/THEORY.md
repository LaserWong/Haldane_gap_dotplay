# A three-purity gap certificate from strips to two dimensions

October 10, 2026.
The analytic derivation and rational recomputation are complete.
An independent audit checked the recurrence and interpolation to all integer square sizes.
The proof has not been formalized in a proof assistant.
The two-dimensional result below follows from simultaneous control of both spatial directions.

## 1. Result and scope

Consider a two-dimensional periodic model with exact selfadjoint thermal-transfer representations in both spatial directions.
A seed consists of three ratios associated with doubling the horizontal length, vertical length, and inverse temperature.
They obey a closed sequential quadratic recurrence.
Finite rectangular heat-trace inputs can therefore give a uniform gap bound for every sufficiently large integer square torus.

Two noncommuting examples illustrate the construction.
The first is a bilayer with two spin-1/2 degrees of freedom per cell and a strong antiferromagnetic rung coupling.
The second is a square-lattice spin-1 model with positive single-ion anisotropy D.
Both horizontal and vertical interactions may be strictly positive.
Conservative analytic heat-trace bounds establish the following results.

- For the bilayer with rung coupling 1 and intralayer Heisenberg coupling g in both directions, 0≤g≤1/4000 gives a unique ground state and Δ_L≥0.151171228506 on every integer square torus L≥2.
- For the spin-1 model with D=1 and Heisenberg coupling g in both directions, 0≤g≤1/6000 gives a unique ground state and Δ_L≥0.152901911246 on every integer square torus L≥2.

These numbers are downward-rounded rational consequences of the sufficient criterion proved here, not estimates of the actual gaps.
No full many-body spectrum is used.
Certified low-energy spectra and tail bounds may replace the analytic seed inputs without changing the recurrence or interpolation proof.

A square seed also covers the common-scale rectangles specified in Section 5.
It does not cover rectangles of arbitrary aspect ratio.
Local weak limits on the infinite plane inherit the corresponding GNS gap inequality.
Finite periodic ground-state uniqueness alone does not establish uniqueness for all infinite-volume boundary conditions.

## 2. Selfadjoint thermal transfers in both directions

### 2.1 A sufficient local structure

Choose a real structure on each finite-dimensional cell such that the intracell term v is real symmetric.
Assume that the intercell interaction in each spatial direction admits the decomposition

$$
-h=\sum_\alpha c_\alpha A_\alpha\otimes A_\alpha,
\quad c_\alpha\ge0,
$$

where A_α is real and the physical h is Hermitian.
Real antisymmetric A_α provide an important special case.
After a whole column of finite width W is treated as one cell, its Hamiltonian remains real symmetric and the intercolumn terms retain an identical-factor decomposition.

Assign a continuous-time history ξ={(t_j,α_j)} to each intercolumn bond.
Absorb the norms ||A_α|| into nonnegative event intensities and normalize the inserted operators to have norm at most 1.
The history measure then has finite total mass.
For left and right histories ξ and ζ, merge their events in time order, insert exp(−τv_W) between consecutive events, and take the column trace.
The resulting kernel k_β,W(ξ,ζ) is real.
Both histories insert the same column operators, so exchanging ξ and ζ leaves the ordered product unchanged except on the measure-zero set of simultaneous events.
Hence

$$
k_{\beta,W}(\xi,\zeta)=k_{\beta,W}(\zeta,\xi).
$$

The normalized insertion bounds give

$$
|k_{\beta,W}(\xi,\zeta)|\le d_W e^{\beta\|v_W\|}.
$$

Together with the finite history measure, this makes X_β,W a real selfadjoint Hilbert–Schmidt operator.
The bondwise Dyson–Duhamel expansion followed by columnwise contraction yields the exact identity

$$
Z(L,W;\beta)=\operatorname{Tr}X_{\beta,W}^{L},\quad L\ge2.
$$

Applying the same construction in the other direction gives the second transfer representation.
Neither positive semidefiniteness of X nor pointwise positivity of its kernel is required.
Even powers give a nonnegative spectrum, while positivity of the partition function determines the sign of the dominant eigenvalue needed for odd-length interpolation.

A periodic direction of length 2 retains two distinct periodic adjacency terms.
Replacing them by a single simple-graph edge changes the finite Hamiltonian and generally invalidates its identification with the square of the same transfer operator.
All small tori here use this periodic multiedge convention.
Length 1 is outside the transfer theorem.

### 2.2 Bilayer and large-D models

For two identical spins s, joint time reversal satisfies (Θ_s⊗Θ_s)^2=1.
An orthonormal basis therefore exists in which joint time reversal is complex conjugation.
Each layer spin takes the form S_a^α=iA_a^α, with A_a^α real antisymmetric, while the rung term S_1·S_2 is real symmetric.
A positive intralayer Heisenberg coupling satisfies

$$
-g\,\mathbf S_{r,a}\cdot\mathbf S_{r+e,a}
=g\sum_\alpha A_{r,a}^\alpha\otimes A_{r+e,a}^\alpha.
$$

The bilayer thus satisfies the sufficient conditions in both directions.

A single spin-1 also has Θ²=1.
Its D(S^z)^2 term is real symmetric in the time-reversal real basis, and positive horizontal and vertical Heisenberg bonds have the same required decomposition.
The square-lattice spin-1 model with D>0 therefore also admits both transfers.

These are sufficient structural conditions for a restricted class of models.
A single half-odd-integer spin has Θ²=−1 and cannot use this real structure directly, although a bilayer or an even-spin block may do so.
A generic tensor-network transfer operator, a completely positive transfer map, or a numerical Trotter approximation cannot be substituted for the exact selfadjoint scalar thermal transfer used here.

### 2.3 Alternating-dimer strips

For a column (y,L/R) of fixed width W, take strong bonds R(x,y)·L(x+1,y), weak intracolumn L·R bonds, and identical vertical couplings on the two sides.
Column time reversal squares to +1.
Let F exchange all L/R pairs simultaneously.
If Fv_WF=v_W, it exchanges the incoming A_L histories with the outgoing A_R histories, and the kernel remains selfadjoint.
This gives a result for every integer axial length at each fixed W.
It supplies no width-uniform constant as W→∞.

## 3. Three purities and their sequential recurrence

Write Z(x,y;b) for the physical partition function.
For even n,m≥2, define

$$
A=\frac{Z(2n,m;\beta)}{Z(n,m;\beta)^2},\quad
B=\frac{Z(2n,2m;\beta)}{Z(2n,m;\beta)^2},\quad
C=\frac{Z(2n,2m;2\beta)}{Z(2n,2m;\beta)^2}.
$$

The ratios A and B are auxiliary density-operator purities in the two spatial directions.
The ratio C is the physical Gibbs purity.
Their defects are a=1−A, b=1−B, and c=1−C.
Define

$$
f(t)=\frac{t^2}{2(1-t)^2}.
$$

Squaring a normalized nonnegative spectrum and renormalizing bounds its purity defect by f(t).
This bound applies separately in all three directions.

Let D_i double x, y, or β and set

$$
P_i(v)=\frac{Z(D_iv)}{Z(v)^2}.
$$

The doubling operations commute.
Cancellation of their partition functions gives

$$
P_i(D_jv)P_j(v)^2=P_j(D_iv)P_i(v)^2.
$$

Since P_j(v)≤1,

$$
P_i(D_jv)\ge P_j(D_iv)P_i(v)^2.
$$

The staircase inputs in the order x,y,β are A,B,C.
Moving the first x edge past y and then β bounds that edge, after the other two coordinates are doubled, by A⁴B²C.
Squaring in x and rotating the staircase repeats the argument for the other edges.
The resulting updates are

$$
a'\le f\!\left(1-(1-a)^4(1-b)^2(1-c)\right),
$$

$$
b'\le f\!\left(1-(1-b)^4(1-c)^2(1-a')\right),
$$

$$
c'\le f\!\left(1-(1-c)^4(1-a')^2(1-b')\right).
$$

The second and third lines use the already updated defects.
The new parameters are (2n,2m,2β).
Specifically, a' controls S_x(2n,2m;2β), b' controls S_y(4n,2m;2β), and c' controls T(4n,4m;2β).

If the three input defects are at most u≤1/100, each product loses at most 7u and

$$
f(7u)\le\frac{49}{2(1-7u)^2}u^2<32u^2\le u.
$$

Each updated defect remains within the same common bound, so the subsequent steps are valid.
Iteration gives

$$
u_j\le\frac{(32u_*)^{2^j}}{32},\quad
(n_j,m_j,\beta_j)=2^j(n_*,m_*,\beta_*).
$$

Doubling only n and β on one strip cannot establish this three-coordinate result.
The third purity supplies the information required to control the growing transverse size.

## 4. One-dimensional interpolation to every integer length

Assume Z_L(t)=Tr X_t^L for every integer L≥2, with X_t real selfadjoint and Hilbert–Schmidt.
For even n, suppose S(n,β)≥1−v and T(2n,β)≥1−v, where v≤1/100.
Then

$$
T(L,\beta)\ge1-4v,\quad n\le L\le2n,
$$

including odd L.

To prove the bound, use T(n,β)≤1 to obtain S(n,2β)≥(1−v)³.
The normalized spectrum of X_2β^n has a unique largest weight.
Its corresponding eigenvalue μ_0 of largest absolute value must be positive, since otherwise the traces of sufficiently large odd powers would be negative.
For a largest probability w≥1/2, purity is at most w²+(1−w)².
If w≤1−2v, this is at most 1−4v+8v², which is strictly below (1−v)³ because the difference is v−5v²−v³>0.
Thus the largest weight exceeds 1−2v.
At v=0 the density operator has rank one and the result is immediate.
The tail ratio at power n consequently satisfies r≤2v/(1−2v).
One spatial squaring also gives S(2n,2β)≥1−5v².
For t=L/(2n)∈[1/2,1], the dominant-eigenvalue estimate and tail ratio yield

$$
Z_L(2\beta)\ge[(1-5v^2)Z_{2n}(2\beta)]^t(1-r).
$$

Hölder interpolation on the absolute spectrum of X_β gives

$$
Z_L(\beta)\le Z_n(\beta)^{2-2t}Z_{2n}(\beta)^{2t-1}.
$$

Their ratio therefore satisfies

$$
T(L,\beta)\ge S(n,\beta)^{2-2t}T(2n,\beta)^t
(1-5v^2)^t\left(1-\frac{2v}{1-2v}\right)\ge1-4v.
$$

The last step uses t∈[1/2,1] and 3/2+5v+2/(1−2v)<4.
The lemma selects a finite temperature for a finite length.
It does not exchange thermodynamic and low-temperature limits.

## 5. Two-dimensional gap theorem for all integer squares

### Theorem

Assume the exact transfer identities of Section 2 hold in both directions for every rectangle whose integer side lengths are at least 2.
Suppose even n_*,m_* and β_*>0 give three purity defects at most 0<u_*≤1/500.
For every j≥0, each integer rectangular Hamiltonian in

$$
2^j n_*\le L_x\le2^{j+1}n_*,\quad
2^j m_*\le L_y\le2^{j+1}m_*
$$

has a unique ground state and obeys

$$
\Delta_{L_x,L_y}\ge
\frac{\log[1/(32u_*)]}{\beta_*}.
$$

When n_*=m_*, this covers every integer square side L≥n_*, including lengths between successive doublings.

### Proof

Fix one seed scale and write u=u_*.
Choose an integer m≤W≤2m and set t=W/m∈[1,2].
For the y transfer at x=2n, the bound B≥1−u gives a unique positive eigenvalue of largest absolute value.
Its normalized weight at power m is at least 1−u and its tail ratio is at most u/(1−u).
Hence

$$
Z(2n,W;\beta)\ge Z(2n,m;\beta)^t
(1-u)^t\left(1-\frac{u}{1-u}\right).
$$

For the y transfer at x=n, monotonicity of the absolute-spectrum ℓ^p norm gives

$$
Z(n,W;\beta)\le Z(n,m;\beta)^t.
$$

The evenness of m makes this valid even when W is odd.
Dividing gives

$$
S_x(n,W;\beta)\ge A^t(1-u)^t\left(1-\frac{u}{1-u}\right)
\ge(1-u)^3(1-2u)\ge1-5u.
$$

The final polynomial difference is u²(9−7u+2u²)≥0.
Apply Section 4 to the y-direction inputs B,C at x=2n to obtain T(2n,W;β)≥1−4u.
At this arbitrary fixed integer W, apply the lemma again in x with common defect v=5u≤1/100.
It follows that

$$
T(L,W;\beta)\ge1-20u,\quad n\le L\le2n.
$$

The largest Gibbs probability is at least the purity and therefore exceeds 1/2.
The ground state is unique, and the probability ratio of the first excited state to the ground state satisfies

$$
e^{-\beta\Delta_{L,W}}\le\frac{20u}{1-20u}\le32u.
$$

Substitute u_j and β_j from Section 3 to obtain the stated j-independent bound.
Both spatial sizes grow together, and interpolation covers every integer side length within each scale.
The bound is consequently uniform as the width increases.

## 6. Analytic seeds without full diagonalization

Let H_0 be a sum of N identical cell Hamiltonians with unique ground states.
Shift each cell ground energy to zero and denote its partition function by z(β).
Suppose V satisfies

$$
\operatorname{Tr}(\rho_{0,\beta}V)=0,\quad
\operatorname{width}(V)\le bN.
$$

The Gibbs variational principle gives Z/Z_0≥1.
Golden–Thompson and Hoeffding's lemma for the spectral probability measure of V in ρ_0 give

$$
1\le Z/Z_0\le\exp[(\beta bN)^2/8].
$$

This argument allows V to fail to commute with H_0.
It does not treat different noncommuting weak bonds as independent classical variables.
In particular, replacing the global N² width estimate by an N estimate requires an additional argument.
For N=nm, the seed bounds are

$$
A\ge e^{-(\beta bN)^2/4},\quad
B\ge e^{-(2\beta bN)^2/4},
$$

$$
C\ge e^{-(4\beta bN)^2/4}z(\beta)^{-8N}.
$$

The last bound conservatively replaces the positive numerator z(2β)^{4N} by 1.

### 6.1 Spin-1/2 bilayer

The Hamiltonian is

$$
H=\sum_r\mathbf S_{r,1}\cdot\mathbf S_{r,2}
+g\sum_{r,e\in\{e_x,e_y\},a\in\{1,2\}}
\mathbf S_{r,a}\cdot\mathbf S_{r+e,a}.
$$

A unit rung has singlet–triplet gap 1 and z(β)=1+3e^{-β}.
The unperturbed Gibbs state factors over rungs, and each individual layer spin has reduced state I/2.
Every weak intralayer bond therefore has zero mean.
Each weak bond has spectral width g, and a periodic N-cell system has 4N weak bonds, giving b=4g.

For n=m=2, β=12, and g≤1/4000, rational exponential intervals give

$$
A\ge0.999424165856154089,\quad
B\ge0.997698652170741851,\quad
C\ge0.990242081527557809.
$$

One exact rational sequential update reaches n=m=4 and β=24, with defect upper bounds

$$
0.000142102218698764,\quad
0.000431988810898762,\quad
0.000830198784090236.
$$

Section 5 then gives Δ_L≥0.151171228506 for every integer L≥4.
For L=2,3, the Weyl spectral-width perturbation bound gives Δ_L≥1−4L²g≥0.991, completing the result for L≥2.

### 6.2 Single-site spin-1 large-D model

Take

$$
H=\sum_r(S_r^z)^2+g\sum_{r,e\in\{e_x,e_y\}}
\mathbf S_r\cdot\mathbf S_{r+e}.
$$

The unperturbed cell ground state is m_z=0 and its excitations are m_z=±1, so z(β)=1+2e^{-β}.
All three spin components have zero mean.
A spin-1 Heisenberg bond has spectrum −2,−1,1 and width 3.
There are two forward periodic bonds per cell, giving b=6g.

For g≤1/6000, β=12, and n=m=2, A and B equal the bilayer bounds, while C≥0.990436793921877631.
After one update, the common defect is at most 0.000796421672766419.
Thus Δ_L≥0.152901911246 for every integer L≥4.
The Weyl bound for L=2,3 is again at least 0.991.

Both examples have noncommuting local terms when g>0.
Their unperturbed product ground states are generally not exact ground states after the perturbation is introduced.

## 7. Limits of fixed-width strip arguments

### 7.1 Positive gaps at each width need not be uniform

Let b_i=σ_i^- and n_i=b_i†b_i be spin-1/2 hard-core operators on a rectangle, periodic in its long direction and Dirichlet in its transverse direction.
Let K be the square-lattice Dirichlet Laplacian and define

$$
H=\sum_{i,j}b_i^\dagger K_{ij}b_j.
$$

This finite-range two-dimensional Hamiltonian has noncommuting terms.
It is also a sum of nearest-neighbor terms (b_i−b_j)†(b_i−b_j) and transverse-boundary number operators.
At width W, K≥λ_W I, where

$$
\lambda_W=2-2\cos\!\left(\frac{\pi}{W+1}\right)>0.
$$

Factorizing the positive matrix K−λ_W I as a matrix square gives H≥λ_WΣ_i n_i.
The vacuum is the unique ground state and a one-particle state attains λ_W.
Each fixed-width gap is therefore exactly λ_W, independently of the periodic axial length.
But λ_W→0, and the infinite plane has one-particle energies approaching zero.
A positive strip gap at every fixed W thus does not imply a uniform two-dimensional gap.

### 7.2 An exact boundary-purity obstruction

Take W independent identical gapped chains, each with a nontrivial finite-temperature transfer spectrum.
The strip transfer is X^{⊗W}, so

$$
S_x(n,W;\beta)=S_{1\mathrm D}(n;\beta)^W.
$$

If S_1D<1 at fixed n and β, this spatial purity decays exponentially in W even though the physical gap is uniform in W.
A two-purity seed threshold at fixed n,β therefore need not hold at arbitrary width.
This is a limitation of the fixed seed geometry, not a theorem of two-dimensional gaplessness.

For independent gapped cells, the physical purity similarly equals [z(2β)/z(β)^2]^N and decays exponentially with volume at fixed β.
Purity near one requires sufficiently low temperature.
Spatial purity also depends on the finite-size curvature of the ground energy, so temperature and seed volume must be chosen together.

The three-purity method still requires computable heat-trace inputs.
It treats the new-direction purity as a separate testable input and grows width, length, and β within the proof.
Finite b_x×b_y blocking may improve the local real structure or finite-size curvature before the same theorem is applied.
The cost is a larger cell dimension and a new check of the identical-factor structure across blocks.

## 8. Relation to other gap methods

`PRIMARY_LITERATURE.md` gives the detailed primary-source comparison.
For frustration-free two-dimensional projector Hamiltonians, local positive gaps and Knabe-type finite-size criteria are natural first tests.
They allow ground-state degeneracy, unlike a criterion requiring purity to approach one.

Local positive-operator decompositions and semidefinite-programming certificates can avoid full large-system diagonalization.
Their outputs require certified positive semidefiniteness, verified local identities, and the appropriate frustration-free or ground-energy assumptions.
The two noncommuting examples here are not frustration-free in their natural local decompositions, so their local gaps cannot simply be inserted into an FF criterion.
The present method instead uses physical heat traces and two selfadjoint transfers.

Convergence of a non-FF finite-volume SDP hierarchy alone does not establish a size-independent two-dimensional thermodynamic certificate.
The three-purity argument provides such a uniform gap under its specific exact-transfer assumptions, which must be checked for each proposed model.

## 9. Recomputing the certificates

`three_purity_certificate.py` uses the Python standard-library `Fraction` type.
Positive Taylor series with rigorous geometric remainders bound exponentials, and reciprocation produces negative-exponential intervals.
Seed purities are rounded downward and recurrence defects upward.
A positive atanh series bounds the logarithm from below, and the final gap is rounded downward.

Running the script rebuilds `bilayer_seed_certificate.json`.
The arguments `--model square_spin_one_large_D --g 1/6000` rebuild `spin_one_seed_certificate.json`.
Floating-point `display` fields in the JSON files are for readability.
Acceptance uses only the rational fields.

Low-energy inputs may call `replay(A,B,C,n,m,beta)` directly.
A success flag certifies the supplied values only together with the mathematical assumptions in this note.
Uncertified floating-point heat traces are not converted into proof by passing this numerical test.

## 10. Choosing the coordinate order

The exchange identity and single-coordinate squaring bound of Section 3 are symmetric in the three coordinates.
Any ordering π=(π₁,π₂,π₃) therefore defines valid staircase inputs at the base point, D_π₁ applied to that point, and D_π₂D_π₁ applied to it.
The same cyclic sequential recurrence holds for these redefined inputs.
The existing numbers A,B,C cannot simply be permuted because their base points differ.

A successful certificate can be converted to the x,y,β order of Section 5 by exchanging adjacent steps.
If the original adjacent purity lower bounds are a=P_i(v) and b=P_j(D_iv), the exchanged true values satisfy

$$
P_j(v)\ge a\sqrt b\ge ab,\quad
P_i(D_jv)\ge a^2b.
$$

The conservative conversion (a,b)↦(ab,a²b) is entirely rational.
At most three adjacent exchanges are required for three coordinates, amplifying the common defect by at most 27.
Additional successful quadratic iterations can then reduce it below 1/500.
Axis labels and base points must be retained throughout the conversion.

For the analytic models of Section 6, let N be the initial cell count and E=(βbN)²/4.
Staircase step k=0,1,2 has perturbation factor exp(−4^k E), since every previous doubling of either spatial volume or β doubles βN.
A temporal step also carries z(β)^(−2N·2^r), where r counts the spatial directions already doubled.
These expressions allow comparison of seeds with the temporal step first, second, or third.

## 11. Infinite-volume interpretation

Suppose a subsequence of square periodic ground states converges locally weakly to ω.
A uniform finite-volume gap δ gives, for each local operator A,

$$
\omega_L(A^*[H_L,A])\ge\delta\bigl(\omega_L(A^*A)-|\omega_L(A)|^2\bigr).
$$

Finite interaction range makes [H_L,A] equal to a fixed local derivation expression once the periodic boundary lies sufficiently far from A.
Taking the local weak limit term by term gives

$$
\omega(A^*\delta_H(A))\ge\delta\bigl(\omega(A^*A)-|\omega(A)|^2\bigr).
$$

The GNS Hamiltonian of this limit state consequently has a gap of at least δ on the orthogonal complement of its cyclic ground-state vector.
Both this orthogonal complement and density of local-operator vectors are understood within this particular GNS representation.
The argument does not place all infinite-volume ground states from different boundary conditions in the same representation or establish global ground-state uniqueness from finite periodic uniqueness alone.

## 12. Small reproducible diagnostics for the obstructions

`toy_checks.py` constructs the 3×W hard-core Dirichlet Laplacian of Section 7.1 for W=1,2,3.
It checks that the two lowest small-matrix eigenvalues reproduce the gap 2−2cos[π/(W+1)].
It also constructs an explicit 2×2 symmetric transfer matrix for a classical Ising chain with a unique all-up ground state and demonstrates the exact s^W spatial-purity dependence for W independent rows.
The generated results are stored in `toy_checks.json`.

These floating-point computations diagnose the formulas and their implementation.
Section 7 provides the analytic proofs of the obstructions.
Acceptance of the three-purity gap certificates does not use the diagnostic floating-point values.
