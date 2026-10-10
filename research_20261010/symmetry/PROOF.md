# Exact symmetry compression and leaked-residual contraction

## Scope and conventions

Ordinary spin-1/2 bilayer, unit vertical AF exchange and equal horizontal/vertical intralayer AF exchange g=p/q>0. Rung lattice is a periodic nx by ny rectangle, N=nx ny. A length-two direction has two parallel edges. Let m_ij be the resulting unordered-edge multiplicity, Q the number of triplet rungs, and E00=-3N/4. The shifted Hamiltonian is

H'=H-E00=Q+(g/2) sum_ij m_ij (T_i dot T_j + D_i dot D_j),

where T_i=S_i,0+S_i,1 and D_i=S_i,0-S_i,1. Thus rung-triplet parity is conserved. This is the ordinary bilayer, without crossed exchanges.

The local unnormalized rational basis has labels 0,1,2,3 for singlet, triplet m=-1,0,+1; its Gram diagonal is (2,1,2,1). The two-triplet singlet |ij> has coefficients (-2,1,-2) on digits (1,3),(2,2),(3,1), with singlets on all other rungs. Divide every global inner product by 2^N. Then vacuum norm is 1, each |ij> norm is 3, and different pairs are orthogonal. The total-spin raising operator annihilates |ij>: S+ t_-=t_0 and S+ t_0=2t_+ give pairwise cancellation. Its total Sz is zero, so it is an SU(2) singlet.

## Exact dimensions and symmetry reduction

The full Hilbert dimension is 4^N, the full Sz=0 dimension is binom(2N,N). With at most two excited rungs, the Sz=0 basis has 1+N+3 binom(N,2) vectors. Its even-triplet-parity part has 1+3 binom(N,2) vectors. The SU(2)-singlet part consists of vacuum and one singlet per unordered pair, so its dimension is 1+binom(N,2).

Sum |ij> over pair orbits under translations and coordinate reflections, adding x/y exchange for square lattices. These orbit sums plus vacuum are independent. Their normalized Gram is diagonal: 1 for vacuum and 3 times the orbit size for each pair sum. On 4x4 there are five pair orbits, represented by unsigned displacement types (0,1),(0,2),(1,1),(1,2),(2,2). Hence the dimensions are 377 -> 361 (even parity) -> 121 (singlet) -> 6 (space invariant). On 2x2 and 4x2 the final dimensions are 3 and 6. On 8x4 and 8x8 they are 15 and 15.

Let P be the full q<=2 projection, including all triplet magnetic states. P commutes with SU(2), parity, and the spatial symmetries. Hence PHP leaves the compressed subspace invariant. The external full-space comparison supplies lambda_1(H)>=a (zero-based eigenvalue indexing). Min-max also gives lambda_1(PHP)>=a. A compressed trial with exact rho<a guarantees an eigenvalue of the compressed restriction below a; it must be the unique eigenvalue of PHP below a, and therefore its smallest eigenvalue. This proves equality of the compressed and full q<=2 Ritz minima, rather than inferring it from numerical agreement. Rounding the two numerical eigenvectors gives different rational Rayleigh quotients; in all nine checked examples their differences were <10^-20.

## Complete q2 action and q4 leakage

For c=c0|vac>+sum_ij cij|ij>, with c_ij=c_ji, the projected action is

(H'c)_0 = (3g/2) sum_ij m_ij c_ij,

(H'c)_ij = (g/2)m_ij c0 + (2-g m_ij)c_ij
             + (g/2) sum_(k != i,j) (m_ik c_kj + m_jk c_ik).

For a four-rung set {i,j,k,l}, the three pairings ij|kl, ik|jl, il|jk have leakage amplitudes

a_(ij|kl) = (g/2)(m_ij c_kl + m_kl c_ij),

and its two analogous expressions. Their normalized Gram matrix has diagonal 9 and off-diagonal 3. These signs were checked directly in the rational local basis, not borrowed from a phase convention. The squared leaked norm on this four-rung set is

6 sum_pairings a_pairing^2 + 3 (sum_pairings a_pairing)^2.

All different four-rung occupation sets are orthogonal. Summing the formula gives the entire omitted q4 norm; no higher q can be reached from q<=2 in one application of H. The same bilinear identity yields the full exact H^2 Gram matrix for multiple trial vectors. The contraction costs O(binom(N,4)) streamed four-rung sets and a small dense orbit matrix. It does not enumerate physical q4 configurations. A sparse graph-based implementation could lower the counting cost further, but is not required for N=64.

## Exact certificate interface

Let B contain the chosen integer-coordinate sparse trial vectors and T=4q(H-E00). All exported matrices are integers:

G=B^*B, K=B^*TB, J=(TB)^*(TB).

The analytic q2 files remove the common factor 2^N from all three matrices. The explicit Krylov files retain it. For an integer coefficient vector v, set n=v^T Gv and e=(v^T Kv)/(4q n). Then

rho=E00+e, residual_squared=(v^T Jv)/((4q)^2 n)-e^2.

The full-Hamiltonian Gram is E00 G+K/(4q). With the separately certified all-sector second-eigenvalue threshold a and rho<a, Temple gives

rho-residual_squared/(a-rho) <= E0 <= rho.

All rational endpoints are saved. Floating diagonalization only proposes v. A small residual is never used as a no-missed-states certificate: completeness still comes from the full-space relative-form bound. The exact tail construction and three-purity recursion are existing separately audited components.

## One block-Krylov extension

The explicit implementation adds H'B to the q2 orbit basis and selects independent columns by exact Gram LDL pivots. On 4x4 the resulting space has dimension 11, remains an SU(2) singlet and spatially invariant, and contains the original 6D space. Its entire H-applied support, including six-triplet configurations, is retained when forming J. The 4x4 union support is 20,081 trial configurations and 452,093 reached configurations. These are representation support sizes, not the number of independent trial vectors or full Hilbert dimension.

At g=.03, the 11D residual squared is 5.315367798234023e-7, versus 1.9285521445631753e-4 for q2 and 1.1199041290423765e-6 for the archived 3,769-dimensional depth-two selected-support calculation. The 11D residual improves both, but its explicit full leaked support costs more than the archived selected-support method. This is not a universal claim that lower linear dimension means lower runtime or memory.

## Larger-depth outlook, not an implemented certificate

On 4x4, all even q<=4 SU(2) singlets have dimension 1+binom(16,2)+3 binom(16,4)=5,581. Pair-matching orbit enumeration gives 81 independent q4 invariant vectors, so vacuum+q2+q4 compresses to 87 vectors. Restricting q4 matchings to two disjoint nearest-neighbor edges gives 9 spatial orbits (400 labeled matchings), hence a 15-vector candidate with the six q2 vectors. Neither candidate has been run or certified here.

For deeper orbit-only implementations, represent each even-q valence matching symbolically. Inner products of two q=6 matchings are 3^(number of loops in their union); q6 has 15 singlet pairings per six-rung set. Only graph-reachable matchings need be generated. Translation/point-group orbit aggregation and streamed pairing contractions could avoid physical-configuration enumeration. At N=64, naively enumerating all six-rung sets (binom(64,6)=74,974,368) is already unattractive, so graph-reachable/orbit-first generation must be estimated before implementation. This is a proposed route, not a validated cost or a completed residual calculation.
