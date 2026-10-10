# Independent proof of the stable quadratic-boson comparison

Updated 2026-10-10 14:31 America/New_York (EDT) / 18:31 UTC.

## Scope and analytical verdict

The proposed stable quadratic comparison is valid for the ordinary periodic spin-1/2 square bilayer at every fixed finite N and 0≤g<1/4. Its ordered spectral bounds remain valid after finite hard-core compression. The directed rational endpoints and finite reference overcount have the correct inequality directions. This review is separate from the sealed bosonic Jacobi review.

The Hamiltonian has vertical coupling one, straight intralayer coupling g in both layers and both lattice directions, and no crossed bonds. Positive-direction periodic edges are counted with multiplicity. In particular, length-two directions have parallel edges. Set H′=H+3N/4 and α=1−2g. All displayed energy bounds concern H′. The complete physical dimension is 4^N.

The independent proof and normalization in `../bosonic_tail_review/PROOF.md` supply an isometric embedding into the Fock space of D=3N modes. If P projects onto at most one boson per rung, Q is the original bosonic total-number operator, K=(g/2)A⊗J, and B=(1/2)Σ K_uv a_u†a_v†, then

H′ ≥ PLP on ran(P),

L = αQ+B+B†.

The inequality is a quadratic-form inequality on the finite-dimensional physical subspace. The projection need not commute with L. The original physical Q is not conserved.

## 1. Stable oscillator realization and its form domain

The real symmetric K has an orthogonal diagonalization K=O diag(κ_j) O^T. The corresponding number-preserving bosonic mode rotation is unitary and preserves Q. For each rotated mode b_j, the comparison operator becomes

L_j = α b_j†b_j + (κ_j/2)(b_j†²+b_j²).

Under the usual finite-mode Fock-space realization on L²(R^D), put b_j=(x_j+ip_j)/sqrt(2), with [x_j,p_k]=iδ_jk. Then

L_j = ((α+κ_j)/2)x_j² + ((α−κ_j)/2)p_j² − α/2.

The weighted graph has degree four, hence ||K||=2g. If 0≤g<1/4, then α>2g and both quadratic coefficients are strictly positive. The quadratic form is therefore bounded below and closed after the usual oscillator form closure. Equivalently, its form norm differs from that of Q+I by bounded positive factors. Every finite-particle vector, including every vector in ran(P), is in this form domain.

Set ω_j=sqrt(α²−κ_j²)>0. The canonical scaling

x_j=sqrt(ω_j/(α+κ_j)) X_j,

p_j=sqrt((α+κ_j)/ω_j) P_j

preserves [X_j,P_j]=i and turns L_j into ω_j(X_j²+P_j²)/2−α/2. The scaling is implemented by a unitary dilation on L²(R). Its dilated Hermite functions form a complete orthonormal eigenbasis. Taking the tensor product of these finitely many mode rotations and dilations gives a unitary U with

ULU† = E_quad + Σ_(j=1)^D ω_j n_j,

E_quad = (1/2)Σ_j(ω_j−α).

This supplies a self-adjoint realization and a discrete complete spectrum. Because min_j ω_j>0 and D is finite, only finitely many oscillator occupation vectors lie below any fixed energy. Thus L has compact resolvent, and form-domain min-max applies to every finite ordered index. No infinite-volume unitary-implementability claim is needed.

## 2. A uniform frequency and ground-shift comparison

Define

δ=sqrt(α²−4g²)=sqrt(1−4g)>0,

v=(1/2)Tr(K²)=(3g²/4)Σ_e w_e².

Then ω_j≥δ. Rationalizing each frequency difference gives

E_quad = −(1/2)Σ_j κ_j²/(α+ω_j)
       ≥ −v/(α+δ) = E_b.

The inequality direction follows because each denominator α+ω_j is at least α+δ, and every numerator is nonnegative. Therefore

ULU† ≥ E_b I + δ Q_ref,

where Q_ref=Σ_j n_j is the total number in the diagonalized reference oscillator basis. This is an operator-form comparison with one equal-frequency reference Hamiltonian. It does not require the first D excited states of the unequal-frequency L to be one-boson excitations. At unequal frequencies, two low-frequency bosons can precede one high-frequency boson. The equal-frequency operator comparison bypasses that ordering issue.

All period-two bond multiplicities enter v through Σ_e w_e². Replacing this expression by Σ_e w_e would underestimate the vacuum-creation norm on such graphs and would invalidate the lower ground-shift bound.

## 3. Ordered min-max after hard-core compression

Let M=4^N. The finite-dimensional form compression of L to ran(P) is a Hermitian M×M operator. For 1≤j≤M, the variational family of j-dimensional subspaces inside ran(P) is contained in the full form-domain variational family for L. Using the increasing ordered-eigenvalue convention,

λ_j(H′) ≥ λ_j(PLP|ran(P)) ≥ λ_j(L).

The first inequality is finite-dimensional form monotonicity. The second is the min-max inequality for a restricted family of trial subspaces. Unitary invariance and the lower reference form then give

λ_j(H′) ≥ λ_j(E_b+δQ_ref).

The equal-frequency reference has energy E_b+qδ and multiplicity

d_q = C(D+q−1,q), q≥0.

Its cumulative count below shell q is

R_q = Σ_(p=0)^(q−1) d_p.

Hence for R_q<j≤R_q+d_q with j≤M,

λ_j(H′) ≥ E_b+qδ.

In particular, d_0=1 and d_1=D=3N yield

λ_1(H′) ≥ E_b,

λ_2(H′) ≥ E_b+δ,

λ_(2+3N)(H′) ≥ E_b+2δ.

These statements count the entire physical spectrum, without fixing magnetization, spin, parity, or momentum. A later retained-band argument must still prove that all of its proposed 1+3N levels lie below the last cutoff and must justify every residual or moment-pencil endpoint it uses.

## 4. Safe finite and infinite tail sums

For β>0, let z=exp(−βδ), so 0<z<1. The nonnegative reference series obeys

Σ_(q≥0) d_q z^q = (1−z)^−D.

The ordered eigenvalue inequality can be applied term by term because the scalar exponential is decreasing. Thus, after a retained band of size k=1+D,

Σ_(j=k+1)^M exp(−βλ_j(H′))
≤ exp(−βE_b)[(1−z)^−D−1−Dz].

The step concerns scalar eigenvalue exponentials. It does not use an incorrect assertion that the matrix exponential is operator-monotone.

A finite overcount is also valid. The original physical basis embeds into original boson-number sectors through q=N, so its dimension is at most the dimension of those sectors. The exact count is

Σ_(q=0)^N C(D+q−1,q)=C(D+N,N)≥4^N=M.

This dimension inequality remains true independently of any later change of basis. The first M entries of the ordered equal-frequency reference list consequently occur no later than shell N. Their positive tail sum is bounded above by including every reference entry through N. Therefore

Σ_(j=k+1)^M exp(−βλ_j(H′))
≤ Σ_(q=2)^N C(D+q−1,q) exp[−β(E_b+qδ)].

No assertion that U ran(P) lies in transformed sectors q≤N is made or needed. The last included shell may contain extra reference levels beyond physical index M. Those extra positive terms only weaken the upper bound. Counting from q=2 removes exactly 1+D reference levels because the reference frequencies are equal.

The reference counts d_q must not be silently replaced by physical triplet-shell counts C(N,q)3^q. The q=2 lower cutoff begins at the same ordered index 2+3N in both constructions, but higher shell indices differ. A future combination of physical-number and reference bins must align their ordered eigenvalue indices before taking the stronger lower bound. It is not valid to take a pointwise maximum at the same q while retaining the smaller physical multiplicities.

## 5. Directed rational endpoint construction

Let g be rational, set x=1−4g>0, and choose rational numbers 0<δ_l<δ_u satisfying

δ_l²≤x<δ_u².

Then δ_l≤δ<δ_u. Set

E_l=−v/(α+δ_l).

The denominator is strictly positive. The map δ↦−v/(α+δ) is nondecreasing for v≥0, so E_l≤E_b. For every integer q≥0,

E_l+qδ_l ≤ E_b+qδ.

Therefore these rational lower endpoints are safe with the same reference multiplicities. This includes g=0, where v=0 and δ=1. The strict condition g<1/4 is essential to a positive frequency and convergent heat trace. At g=1/4 the displayed compact-resolvent and finite-temperature arguments do not apply.

The producer's decimal square-root procedure sets s=10^40 and k=floor(s sqrt(x)) via the integer square root of floor(x s²). This is valid because floor(sqrt(floor(y)))=floor(sqrt(y)) for y≥0. The frozen acceptance uses the directly checked squared inequalities, not floating values. This review additionally constructs an independent 160-bit binary root interval and verifies compatibility.

Any future finite-tail evaluation can avoid cancellation by summing its positive q≥2 terms with outward exponential bounds. An implementation of the closed infinite expression must direct both the subtraction and the reciprocal-power enclosure correctly. This review certifies the bin endpoints and multiplicities, not a future trace evaluation.

## 6. Independent exact checks and limits

The frozen input is `low_band/quadratic_boson/FROZEN_MANIFEST_1828.json`, SHA-256 `ac5c47a1a3ccff0962b7ad5aac3968834b9ff06026644e0abc56601bec750723`. The snapshot includes 14 bin records, the producer's physical tests, and its proof and code. Every byte hash is checked before and after replay.

The executable imports only a copied independent audit helper, whose complete source is stored as `independent_base.py`. No producer module is imported. The small-mode checks use positive and negative pairing strengths, and a rationally rotated two-mode K with unequal frequencies. Exact factorial metrics and rectangular source-to-image matrices retain all one-step leakage. The checks verify the canonical commutation relations, the oscillator factorization, and positivity above E_b. Their source cutoffs are testing devices and are not substituted for the analytic infinite-Fock-space proof.

The physical checks reconstruct the ordinary bilayer exchange from the orthonormal four-spin computational representation and assemble all 256 states of the 2×2 model. Exact parity and Sz blocks account for every state. At both g=.03 and g=.06, rational inertia checks H′−PLP≥0 and counts the physical and compressed-comparison eigenvalues below every relevant reference threshold. These are exact finite-size checks of the normalization, compression direction, and counting implementation. They do not establish the general theorem by extrapolation.

The 14 bin records cover 2×2 at g=.03,.06 and 4×4,8×4,8×8 at g=.03,.04,.05,.06. Every rational endpoint, squared root inequality, multiplicity, first index, total reference count, energy shift, and graph normalization is independently recomputed. Float displays are diagnostic only. No retained-band endpoint, heat trace, recurrence, finite-size bridge, or global gap is upgraded by this tail-only review.

Run `bash REPRODUCE.sh` to repeat the checks. Execution is pinned to one CPU, all numerical-library thread counts are one, and address space is limited to 1.5 GiB. Outputs stay in this review directory and no remote state changes occur.
