# Full-space ground inverse-moment pencil

Checkpoint: 2026-10-10 14:55 America/New_York / 18:55 UTC.
Status: exact arithmetic candidate; independent review pending.

This directory changes no existing physical input or prior certificate. It uses
only the already audited G, A and B matrices of the 11/29-dimensional ground
trial spaces. In particular, it adds no physical trial states, no H²-applied
states, and no moments beyond the stored full B=(HW)*HW.

## Theorem with more trial directions than low levels

Let H be a finite-dimensional Hermitian operator on an invariant sector. Assume
that this sector has exactly k eigenvalues, counting multiplicity, strictly
below a. Eigenvalues equal to a are allowed. Let W have m independent columns,
with exact complete moments

    G=W*W, A=W*HW, B=(HW)*(HW).

The matrix B includes all leakage of HW outside the span of W. Define

    K=A-aG, S=B-2aA+a²G.

Assume S is positive definite. Do not require K to be negative definite, and do
not identify the number m of trial directions with the external low count k.
Let μ₁≤…≤μᵣ<0 be the negative eigenvalues of the Hermitian generalized pencil
(K,S). There can be at most k of them. If the sector eigenvalues below a are
λ₁≤…≤λₖ, then for each j=1,…,r,

    λ_(k+1-j) ≥ a+1/μⱼ.

For a rational candidate l<a, an entirely exact sufficient test is

    negative_inertia[B-(a+l)A+alG] ≥ j.

It proves λ_(k+1-j)>l. In the ground application k=1, m=11 or 29, and the test
requires one negative eigenvalue, not negative definiteness of the full pencil.

### Proof, including eigenvalues at the cutoff

Set X=(H-a)W and M=(H-a)†, the Moore–Penrose inverse. Then X*X=S, so X has m
independent columns. The identities of the spectral calculus give

    X*MX = W*(H-a)(H-a)†(H-a)W = W*(H-a)W = K.

These identities hold also at an eigenvalue equal to a: the corresponding
spectral component vanishes on both sides. M has exactly k negative eigenvalues,
ordered as

    νⱼ=1/(λ_(k+1-j)-a), j=1,…,k.

Its remaining eigenvalues are zero or positive. The Ritz min-max principle on
ran X gives νⱼ≤μⱼ. Thus r≤k, and taking reciprocals of negative numbers gives
1/μⱼ≤1/νⱼ, which proves the claimed bound.

The endpoint matrix is S+(a-l)K. Congruence with S^(-1/2) shows that its negative
inertia counts exactly the μ-values strictly below -1/(a-l). At least j such
values imply μⱼ<1/(l-a), hence l<a+1/μⱼ≤λ_(k+1-j).

For k=1, a shorter proof of the acceptance test does not even require S>0:
if λ₁≤l and every other sector eigenvalue is at least a, then
(H-a)(H-l) is positive semidefinite. Its compression to W is the endpoint
matrix, which could not have a negative direction. The S>0 test is retained in
the implementation to justify generalized-eigenvalue proposals and optimization.
G>0 confirms independence; neither G>0 nor S>0 establishes the external count.

## Relation to the previous scalar Temple bound

Any coefficient vector c with Rayleigh quotient θ<a and complete residual
squared r² has

    (c*Kc)/(c*Sc) = (θ-a)/[(θ-a)²+r²] < 0,
    a + (c*Sc)/(c*Kc) = θ-r²/(a-θ).

The smallest generalized eigenvalue μ₁ is at most this scalar quotient. Since
x↦1/x is decreasing on the negative half-line, the optimized full-space bound
a+1/μ₁ is at least the scalar Temple bound computed from the same c and cutoff.
All stored previous ground vectors remain in W; no new physical input is needed.
The actual endpoint is rounded down and accepted by exact rational inertia.

## External low-count proof used for these bilayer patches

The ordinary spin-1/2 bilayer has unit rung coupling, equal straight in-layer
g≥0, periodic weighted edges, N rung pairs, and shifted Hamiltonian H'=H+3N/4.
All matrices and energies here are for H'. The cited quadratic-boson comparison
provides full-space ordered lower bounds a₀, a₁ and a₂ with

    λ₁(H')≥a₀, λ₂(H')≥a₁, λ_(2+3N)(H')≥a₂.

The previously independently audited ground trial has θ<a₁. It therefore
identifies the unique global ground state. Its entire 11/29-direction trial
space lies in the invariant even triplet-parity sector. The audited N
translated spin-one directions, with spin multiplicity 3, lie in odd parity.
Their complete G/A/B data and invariant-sector structure have been verified
elsewhere; the current producer rechecks their saved Ritz upper endpoints <a₂.

The even ground direction and the 3N odd triplet directions thus supply 1+3N
independent trial directions with their Ritz operator below a₂. Full-space
min-max counting gives exactly 1+3N eigenvalues below a₂. At least 3N of these
belong to odd parity. The even sector consequently has exactly one eigenvalue
below a₂, and it is the global ground. This supplies k=1 and a=a₂ for the
present theorem. It makes no false inference from the size of the ground trial
space or from a small residual. A separate parity-resolved bosonic proof is not
required for these records.

Dependencies: `../quadratic_boson/QUADRATIC_COMPARISON.md`, the independent
`../../quadratic_boson_review/PROOF.md`, complete band review
`../../large_seed_review/REVIEW.md`, and new-coupling review
`../../bilayer_frontier_review/REVIEW.md`. The per-patch source hashes identify
the exact moments, cutoff bins and complete-band endpoints actually used.

## Implementation and meaning of the output

`certify.py` checks G>0, S>0 and exactly one negative direction of K in each
physical case. It produces a floating proposal only from the small pencil and
then accepts the lower endpoint using fraction-free integer inertia of the
rational endpoint matrix. An upper bracket with zero negative inertia records
the numerical optimum of this particular pencil. That bracket is not a
physical upper energy bound. The physical upper energy remains the previous
exact Rayleigh quotient.

The proposed complete-band `temple_*.json` records replace only the ground lower
endpoint. Triplet intervals, Rayleigh upper endpoints, whole-spectrum bins and
all dimensions remain unchanged. Every result stays a candidate pending its
own independent review; the existing frozen sources are not overwritten.

Each ground endpoint also has an explicit integer coefficient vector c with

    c*[B-(a+l)A+alG]c < 0

as an exact rational inequality. This negative-direction witness is a second
acceptance route that does not depend on trusting the integer inertia routine.
The coefficients specify a direction inside the same stored 11/29-dimensional
space. They do not require a new sparse-state expansion or a new moment.

`validate.py` includes 34 exact finite-matrix tests with nonorthogonal trials,
more trial directions than low levels, cutoff eigenvalues and full leakage. It
also checks rejection when S is singular, the generalized-k indexing when only
part of the low subspace is represented, and a counterexample to discarding the
external low-count hypothesis. These producer tests are not an independent
physical audit.
