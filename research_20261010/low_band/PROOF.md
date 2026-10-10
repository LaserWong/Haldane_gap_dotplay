# Exact full-low-band certification

Updated 2026-10-10 13:20 America/New_York / 17:20 UTC.

This note proves the finite-dimensional method used by `low_band_certificate.py`.
It does not infer spectral completeness from small residuals.
The full-space eigenvalue count comes from the previously certified local relative-form inequality.
The method and new numerical certificates are research results pending independent review.

## 1. Complement compression from a globally counted low band

Let H be a self-adjoint operator on a finite-dimensional Hilbert space.
Write its eigenvalues in increasing order as λ₁,…,λ_D, including multiplicity.
Let Q have k orthonormal columns, let T=Q*HQ, and let R=HQ−QT.
Suppose exact bounds establish

- λ₁ ≥ L₀
- λ_{k+1} ≥ a
- T ≤ rI with r<a
- R*R ≤ εI

Set δ=a−r, σ²=min{1,ε/δ²}, and b=a−(a−L₀)σ².
Then the compression of H to ran(Q)⊥ obeys

    Q⊥* H Q⊥ ≥ bI.

Here Q⊥ denotes any orthonormal basis of the orthogonal complement.
The construction requires no explicit Q⊥.

Proof.
The min-max principle gives λ_k≤λ_max(T)≤r<a.
Consequently H has exactly k eigenvalues below a.
Let P denote their spectral projector and let H_+ be the restriction of H to ran(I−P).
Then H_+≥aI.
For X=(I−P)Q, the residual equation becomes

    H_+ X − XT = (I−P)R.

The solution is the convergent integral

    X = ∫₀∞ exp[−t(H_+−rI)] (I−P)R exp[t(T−rI)] dt.

Differentiating the integrand proves the equation, and the operator norm of the integrand is at most exp(−tδ)||R||.
Hence ||(I−P)Q||≤√ε/δ.
For two projections of equal rank, the principal-angle identity gives

    ||P(I−QQ*)|| = ||(I−P)Q||.

This identity follows, for example, by singular-value decomposition of the k×k overlap matrix between orthonormal bases of their ranges.
Thus a unit vector u orthogonal to ran(Q) has ||Pu||²≤σ².
Since P commutes with H,

    ⟨u,Hu⟩ ≥ L₀||Pu||² + a||(I−P)u||²
             ≥ a−(a−L₀)σ² = b.

This proves the result.
The statement is useful only when the external count a lies above the complete trial band.
A missing low state invalidates that prerequisite even when a selected trial vector has zero residual.

The separated-spectrum integral argument is also presented in J. A. Tropp, Matrix Analysis, Caltech ACM 204 lecture notes, Corollary 11.12, https://tropp.caltech.edu/notes/Tro22-Matrix-Analysis-LN.pdf .
The proof above is self-contained and fixes the one-sided separation needed here.

## 2. Rational Gram data avoid algebraic orthonormalization

Let W be any full-rank rational trial matrix in a rational orthogonal basis with positive diagonal metric J.
Define

    G=W*JW,  A=W*JHW,  B=(HW)*J(HW).

The conceptual orthonormal basis Q=WG^{-1/2} is never computed exactly.
The compressed operator is congruent to the pencil A−tG, so its exact eigenvalue counts follow from the inertia of that rational matrix.
The true residual Gram before normalization is

    Γ = B−AG^{-1}A.

For any rational coefficient matrix D, define

    E = (HW−WD)*J(HW−WD)
      = B−AD−D*A+D*GD.

Orthogonal projection can only decrease the squared norm.
Therefore Γ≤E, and the exact PSD inequality E≤εG implies R*R≤εI.
The implementation uses a diagonal rational D proposed from floating Ritz values.
It verifies G≻0, E≥0, and εG−E≻0 by exact integer congruence and fraction-free inertia.
Thus neither numerical eigensolver accuracy nor a floating Gram orthogonalization enters acceptance.

The map HW must be evaluated on every reached configuration, including all states outside the trial support.
The implementation constructs that full rectangular map before forming B and E.
Every coefficient accumulation and Gram product uses arbitrary-size Python integers.
Stored int64 trial vectors are only input data and are promoted before products.

## 3. Schur-polynomial lower bounds on all retained eigenvalues

Assume the complement bound from Section 1 gives b>r.
For t<b, block decomposition in ran(Q)⊕ran(Q)⊥ gives

    H−tI = [[T−tI, R*], [R, C−tI]],   C≥bI.

Because C−tI is positive definite, inertia additivity under exact congruence reduces the negative count to the Schur complement

    S(t)=T−tI−R*(C−tI)^{-1}R.

The inequalities C−tI≥(b−t)I and Γ≤E imply

    S(t) ≥ G^{-1/2}[A−tG−E/(b−t)]G^{-1/2}.

Consequently the number of eigenvalues of H strictly below t is at most the negative inertia of

    F(t)=(b−t)(A−tG)−E.

If this inertia is at most i−1, then λ_i(H)≥t.
The Ritz variational principle supplies λ_i(H)≤θ_i, and exact inertia of A−tG provides rational upper bounds on θ_i.
The implementation proposes t using a small floating augmented matrix and accepts it only after exact inertia of F(t).
Thus a floating square root used to propose this endpoint is harmless.

The same argument applies blockwise when H has exactly invariant, mutually orthogonal symmetry sectors.
Our trial blocks have dimensions k_j and all their Ritz values are below b.
The variational principle therefore gives at least k_j low eigenvalues in each represented sector.
The global full-space count permits only k=Σk_j eigenvalues below b because b≤a and λ_{k+1}≥a.
Each represented sector therefore has exactly k_j such eigenvalues, and no omitted sector contributes another one.
This justifies using the blockwise enclosures with their full multiplicities.

## 4. Ordinary square bilayer and whole-Hilbert-space count

The model has N=nx·ny spin-1/2 rungs with unit antiferromagnetic rung coupling.
Both straight in-layer directions have coupling g.
There are no crossed exchanges.
Periodic positive-direction edges retain their multiplicity, including parallel bonds when a side length is 2.
The constant energy shift is E00=−3N/4.
Write H'=H−E00I.

The exact local relative-form certificate establishes

    H' ≥ αN_triplet−BI,   α>0.

For this model the isolated-rung spectrum is 0 with multiplicity 1 and 1 with multiplicity 3.
Therefore the full generating function is (1+3x)^N.
The ordered comparison, across every spin and magnetization sector, gives

    λ₁(H')≥−B,
    λ_{2+3N}(H')≥2α−B.

The trial band has k=1+3N dimensions.
It contains one even-triplet-parity M=0 trial, N odd-parity M=0 trials, and N odd-parity M=+1 trials plus their spin-reversed partners.
Global spin reversal commutes with H and maps M=+1 to M=−1, so the last block has multiplicity two.
Total magnetization and global layer-exchange parity are exact symmetries.
Since N is even for all seed patches, this layer-exchange parity equals triplet-number parity.
The code independently checks every accumulated matrix transition for both magnetization and parity.

The complete full-space band count does not rely on calling individual numerical states spin triplets or on identifying their total-spin labels.
The preserved sector ranks and the global ordered-bin inequality suffice.

## 5. Full-low-band heat traces and seed numerators

Let l_i≤λ_i(H')≤u_i for i≤k be the certified complete band, including all multiplicities.
Choose the rational ground upper endpoint u₁ as the trace shift.
For β≥0 define q_N(β)=exp(βu₁)Tr exp(−βH').
Then

    Σ_{i≤k} exp[−β(u_i−u₁)] ≤ q_N(β)

and

    q_N(β) ≤ Σ_{i≤k} exp[−β(l_i−u₁)]
             + exp[β(B+u₁)] Σ_{j=2}^N C(N,j)3^j exp(−βαj).

The tail starts at j=2 only because completeness of all k=1+3N low states has been established.
The implementation evaluates the positive tail sum directly, avoiding unsafe subtraction of outward-rounded exponential quantities.
Every exponential endpoint uses the existing rational Taylor-remainder routine.

Let e_N=E00_N+u₁,N.
For patches 2×2, 4×2 and 4×4, respectively labeled 4,8,16 by their rung count, the exact lower inputs are

    A ≥ exp[−β(e₈−2e₄)] q₈,lower(β) / q₄,upper(β)²,
    B ≥ exp[−β(e₁₆−2e₈)] q₁₆,lower(β) / q₈,upper(β)²,
    C ≥ q₁₆,lower(2β) / q₁₆,upper(β)².

All three numerators retain the complete certified low band.
The existing exact three-purity bootstrap consumes the resulting downward-rounded rational endpoints.
The finite certificates alone do not establish a thermodynamic gap.
A successful replay must be combined with the already audited transfer theorem and its stated size scope.

## 6. Sharper all-spectrum bins from triplet-number compressions

The affine comparison is valid but loses too much on the two-triplet tail at g=0.03.
A second full-space comparison uses the tridiagonal structure in total triplet number.
All statements below assume g≥0 and the periodic degree-four rung multigraph of Section 4.

For one weighted rung edge, let v denote the sum of the two straight spin exchanges at unit coupling.
Its number-preserving part obeys

    v_pres ≥ −(n_i+n_j)/2.

Indeed, in the zero-triplet sector it vanishes.
In the one-triplet sector it is a hopping operator with eigenvalues ±1/2.
In the two-triplet sector it is (T_i·T_j)/2, with lowest eigenvalue −1.
The code also verifies the combined sixteen-dimensional rational matrix inequality by exact inertia.
Summing the edge inequalities, with degree four including multiplicity, gives

    H'_{q,q} ≥ (1−2g)q I.

The number-changing part connects q only to q±2.
In an orthonormal rung basis, each creation from an empty edge has three possible triplet-pair outputs, each of coefficient magnitude g/2.
Each annihilation from an occupied edge contributes at most one matrix entry of magnitude g/2.
The code checks all three squared normalized coefficients as exactly 1/4 for unit g.
Parallel edges are counted with their positive weights and cannot defeat the triangle inequality.

Let E_occ,max(q) be the maximal total occupied-edge weight among all q-element rung subsets.
The maximal empty-edge weight satisfies

    E_empty,max(q)=2N−4q+E_occ,max(q).

This follows by separating occupied-occupied, occupied-empty and empty-empty edges and using degree four.
For the rectangular block K_q=P_{q+2}H'P_q, absolute row and column sums therefore give

    ||K_q||² ≤ ||K_q||₁ ||K_q||∞
             ≤ (3g²/4) E_empty,max(q) E_occ,max(q+2) = t_q².

All maxima are obtained by integer enumeration of 2^N occupation subsets for the current N≤16 patches.
Their values, graph edges, witnessing subsets and degree checks are stored in `number_bins_*.json`.
No spin eigenstates are discarded by this enumeration.

For an arbitrary cutoff q₀, compress H' to the subspace with triplet number at least q₀.
For any vector ψ in that subspace, put x_q=||P_qψ||.
Its quadratic form is bounded below by

    Σ_{q≥q₀}(1−2g)q x_q² − 2Σ_{q≥q₀}t_q x_q x_{q+2}.

The scalar comparison splits into both parity chains, starting at q₀ and q₀+1.
Let a_{q₀} be a common lower bound for their two smallest eigenvalues.
It follows that the compression is at least a_{q₀}I.
This subspace has codimension

    d_{<q₀}=Σ_{j<q₀} C(N,j)3^j.

The min-max principle gives the full-space ordered-bin inequality

    λ_{d_{<q₀}+1}(H') ≥ a_{q₀}.

The removed coupling to low-number sectors does not invalidate this conclusion.
A codimension-d compression has lowest eigenvalue at most λ_{d+1}(H'), which is precisely the direction needed.

The irrational entries t_q need not be represented in exact arithmetic.
For each proposed rational a, positive definiteness of either scalar Jacobi chain is equivalent to the positive rational LDL pivots

    p₀=(1−2g)q₀−a,
    p_j=(1−2g)(q₀+2j)−a−t_{q₀+2j−2}²/p_{j−1}.

Each pivot is recorded exactly.
Taking the minimum over the two chains establishes a_{q₀}.
The bounds may also be monotonized by replacing a_q by max_{j≤q}a_j, since ordered eigenvalues are nondecreasing.

These bins replace the affine tail in Section 5 by

    tail ≤ Σ_{q=2}^N C(N,q)3^q exp[−β(a_q−u₁)].

They also replace L₀ by a₀ and the band cutoff a by a₂ before recomputing the complement and Schur enclosures.
For the 4×4, g=3/100 patch, the certified values are

    a₀ = −0.011528905095,
    a₁ =  0.919897515950,
    a₂ =  1.844298248746.

All displayed decimals here are exact rational endpoints with denominator 10^12.

## 7. Correlated first bootstrap step

Multiplying separately bounded A, B and C loses cancellations.
For the canonical spatial-spatial-temperature staircase, direct trace identities give

    J₁=A⁴B²C=Z₁₆(2β)/Z₄(β)^8,
    J₂=B⁴C²=Z₁₆(2β)²/Z₈(β)^8.

The code bounds these ratios directly with the same certified low-band trace intervals, preserving the complete low-band numerator at 2β.
Let G(x)=1−(1−x)²/(2x²).
The first whole doubling cycle is bounded by

    A₁≥G(J₁),
    B₁≥G(J₂ A₁),
    C₁≥G(C⁴ A₁² B₁).

Every right-hand side is evaluated with exact rational downward rounding and is used only while it is positive.
The saved canonical-order successes use the existing audited three-purity replay after this first step.
Other staircase orders are diagnostic candidates until their matching transfer/interpolation statement is reviewed.
