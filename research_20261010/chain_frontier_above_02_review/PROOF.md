# Independent expanded-reference chain theorem

Updated 2026-10-10 17:25 EDT (America/New_York) / 21:25 UTC.

## Physical conventions and independent reconstruction

For periodic spin-one cells, H_M is the sum of M unit strong bonds and M weak bonds with coefficient g. Both geometrically distinct weak links are retained at M=2. Set H'=H_4+8I=E+gV. Strong-dimer energies are 0,1,3 with multiplicities 1,3,5. The nine rational Clebsch–Gordan columns in physical magnetic coordinates are mutually orthogonal, have Gram weights 3,2,2,2,1,2,6,2,1, and are independently checked as strong-bond eigenvectors. The spin-one ladder factors sqrt(2) cancel the 1/2 in the flip-flop interaction. The exact local weak operator is constructed from these physical one-spin matrices, including all nine dimer states.

P is the complete product reference subspace E<3. Enumeration over all 9^4 physical reference states gives rank(P)=1+12+54=67 and rank(Q)=6494. This is an orthogonal projector after division by the strictly positive diagonal Gram metric, not an assumed orthonormal integer basis. Every one of the twenty single-quintet configurations is in Q at energy 3.

For all 67 columns the verifier constructs the full untruncated weak action. It forms K=P*VP and J=P*V²P using exact physical metric weights. Independently, it constructs R directly from all leaked configurations in Q. It then checks every entry of R=J−KG⁻¹K. Thus g²R is the full H' residual Gram. Couplings into quintets and all off-diagonal residual entries are retained. It separately verifies all magnetic block zeros before using magnetic blocks to accelerate exact congruence.

For each rational local comparison gV_local+a(h_i+h_j)+bI>0, a fresh rational positive-pivot factorization of the full 81-dimensional physical Gram-congruent matrix proves the form inequality. Summing over four links gives H'≥αE−B with α=1−2a>0 and B=4b. Its compression to Q is C≥cI with c=3α−B. This uses weighted dimer energy, not occupancy.

## Counted Schur theorem without an isolated Ritz band

Write H' in the P,Q orthogonal decomposition as [[D,B*],[B,C]], with C≥cI. For t<c, C−t is positive definite, and exact Schur congruence gives

n_−(H'−t)=n_−(D−t−B*(C−t)⁻¹B).

Since (C−t)⁻¹≤(c−t)⁻¹I, the Schur complement on the right is bounded below by D−t−B*B/(c−t). Negative inertia reverses this order. Therefore

#{physical eigenvalues <t} ≤ n_−(D−t−B*B/(c−t)).

In the rational, unnormalized reference coordinates, positive multiplication by c−t and Gram congruence yield the exact matrix

F(t)=(c−t)(diag(E)G+gK−tG)−g²R.

The new verifier computes its inertia with rational symmetric congruence, independently of the producer's integer fraction-free inertia routine. A nonzero diagonal pivot contributes its exact sign; if all diagonal entries vanish but the matrix is nonzero, a nonzero off-diagonal 2×2 block has one positive and one negative eigenvalue and is eliminated exactly. An all-zero remaining matrix contributes its full nullity. This covers indefinite matrices and zero-pivot cases without numerical tolerances.

For ascending saved thresholds t_j<c, the verifier proves n_−(F(t_j))=k_j and nullity zero, starting k_0=0. Consequently λ_(k_j+1)(H')≥t_j; by monotonicity the same bound covers the next k_(j+1)−k_j ordered levels. These are counted lower endpoints, not measured spin-sector multiplicities. The final bin ends at index 67. The global min–max comparison H'≥αE−B supplies every ordered index ≥68, with exactly the multiplicities of reference energies E≥3. No claim that 67 physical eigenvalues lie below c is needed. Nor is commutation of D and B*B needed.

The independently certified ground lower endpoint e_-+8 replaces only the first endpoint after checking that the first counted bin has multiplicity one and t_0<e_-+8<t_1. The full-space ground enclosure and uniqueness are independently replayed by the sealed earlier physical action verifier. No compressed Ritz value is used as a physical lower eigenvalue.

## All-temperature trace and complete counting

The coefficients d_e of (1+3x+5x³)^4 enumerate all 6561 states. For every β≥0, the unshifted trace normalized by the ground Rayleigh upper endpoint ρ satisfies

exp(βρ)Z_4(β) ≤ exp(β(ρ−e_-)) + Σ_(counted bins after ground) m_j exp(−β(−8+t_j−ρ)) + Σ_(e≥3) d_e exp(−β(−8+αe−B−ρ)).

Exactly 1+66+6494=6561 ordered eigenvalues are accounted for. No physical energy-sector invariance, occupancy parity, or low-band separation is assumed. The endpoint theorem proves this for all β≥0, while a finite list of β values is selected for the gap certificates. Exponentials are enclosed by a 110-term Taylor remainder with directed 384-bit dyadic rounding; there is no floating acceptance step.

## Largest seed and all-integer continuation

The M=8 input uses only a rational Rayleigh expectation from the sealed independently checked two-vector Gram/strong/weak matrices. It contributes exp(−2βρ8) as a lower bound on Z8(2β). Its physical dimension is 9^8=43,046,721; trial support is 43,294; linear combination space is dimension two. No M=8 residual, spectral tail, low band, or additional physical-state search is required. These dimensions are not MPS bond dimensions.

Using the complete M=4 trace gives rational lower bounds for J=Z8(2β)/Z4(β)^4 and C=Z8(2β)/Z4(2β)^2. The sealed independent joint-ratio recurrence and signed-transfer finite-window theorem apply with the same Hamiltonian normalization. The initial joint relation S²T≥J, with S,T≤1, gives S≥sqrt(J), T≥J at (4,β), establishing every integer size in [4,8], including odd sizes.

The independent scalar replay checks all time-first and canonical steps, retained joint products, every [8,16],[16,32],… window, and the exact match to the terminal all-integer asymptotic onset. Every proposed gap is tested with an outward exponential witness. M=2,3 are bridged directly by the product singlet and local form bound: λ2(H_M)≥−2M+1−2a−Mb and E0≤−2M, hence gap≥1−2a−Mb>0. The final certificate is the minimum over both short sizes, every finite window, and the asymptotic theorem, and implies unique finite-volume ground states.

These certificates concern only the explicitly listed discrete couplings. They assert neither a continuous coupling interval, an optimal frontier, a physical phase transition, the actual gap, nor infinite-volume uniqueness. Failure of a finite β scan is not an all-temperature impossibility.

## Separate all-temperature obstruction at g=1/4

This result concerns only the saved 67-dimensional denominator certificate and saved two-vector M=8 Rayleigh numerator, followed by their fixed initial time-first purification and mandatory [8,16] window. Let J_rec,C_rec denote the ideal unrounded outputs of this recipe; any downward-rounded implementation is no larger. These are certified lower endpoints for physical ratios. The following ceilings are on the recipe outputs, not on the physical ratios themselves.

Write δ=ρ8−2ρ4>0 and d=−8+t_triplet−ρ4>0. The saved trace upper expression Q_upper(β) contains a ground term at least one and the first counted multiplicity-three term 3 exp(−βd). Hence

J_rec≤exp(−2βδ)/(1+3 exp(−βd))⁴,
C_rec≤exp(−2βδ)/(1+3 exp(−2βd))².

Using a rational δ_lower≤δ and d_upper≥d weakens both ceilings in the safe direction. On each [l,h], numerator exp(−2βδ)≤exp(−2l δ_lower), while denominator lower bounds use h d_upper. Capping the endpoints at one is valid because a recipe lower endpoint cannot exceed the actual ratio, which is at most one. The purification map G(x)=1−(1−x)²/(2x²) is increasing for 0<x≤1. Thus z=C_rec² max(0,G(J_rec)) is bounded by the interval expression checked independently.

All 1,200 rational intervals of width .01 cover [0,12]. Fresh 384-bit/110-term directed exponential enclosures verify every saved interval ceiling; their maximum is 0.4970915063143724<1/2. For β≥12, C_rec≤exp(−2βδ_lower) and max(0,G(J_rec))≤1, so z≤exp(−48δ_lower)<0.472341<1/2. The .25 ground Rayleigh and M=8 expectation are also independently replayed.

If either initialized purity bound is nonpositive, the recipe has already failed. Otherwise a=G(J_rec)≤1 and b=G(z)<G(1/2)=1/2. Its transported thermal bound T=a²b<1/2 cannot make the mandatory [8,16] signed-transfer purity lower bound exceed 1/2 (that lower bound is no larger than T). This blocks a positive gap certificate through this fixed early window for every β≥0, regardless of subsequent rounds. It does not exclude improved physical inputs, different trial vectors, a different initial inequality, or an independent early-size bridge. It is not a statement about the actual gap or physical purity.
