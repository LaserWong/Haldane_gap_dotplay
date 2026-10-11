# Hard-core pair product: exact ansatz, obstruction, and contraction gates

2026-10-10 21:08 EDT / 2026-10-11 01:08 UTC. Local theoretical/cost assessment only. The only executed new calculation is a geometry-only integer/rational check (under one CPU second, CPU6). No new 8x4 state, support pass, physical endpoint, or gap is produced. This directory is not an independent physical review.

## Decision first

Do not launch the nearest-neighbor one-parameter pair product as a replacement ground seed. Although it completes all disconnected pair-creation sectors, it omits a necessary order-g² two-triplet component. At g=11/100 and the first-order parameter z=-g/4, its COMPLETE variance is rigorously at least .00546193724. This follows from a certified norm upper bound, not an assumption that the vacuum dominates. It is already much larger than the accepted 57D variance scale. This is an exact obstruction at that z, plus a perturbative diagnosis; it is not a global optimization exclusion for every real z or every dressed ansatz.

A one-marked-pair correction is more defensible than exponentiating all 14 pair orbits. Even then, contraction feasibility needs a state-count gate; formal PEPS dimension four does not establish a cheap exact torus contraction.

## 1. Model and exact ansatz

Use the accepted physical convention H'=Q+(g/2)A, A=C+C†+D on N=32 rungs. In spherical triplet basis a=1,2,3, J_ab=s_a delta(b,4-a), s=(-1,+1,-1). The unnormalized invariant pair is Ω_ij=Σ_ab J_ab |a_i b_j>, with norm squared 3. Define b†_ia=|a><s| and P†_ij=Σ_ab J_ab b†_ia b†_jb. Aggregate positive-direction periodic parallel edges before all products: C†=Σ_e w_e P†_e. There is no sqrt(3) or g in C†. This is precisely the accepted convention.

All pair creators commute. For intersecting edges both orders vanish, by the local hard-core identity b†_ia b†_ib=0; for disjoint edges they commute. Also (P†_e)²=0. Consequently, for real z,

  ψ(z)=exp(zC†)|0>= product_e (1+z w_e P†_e)|0>
       =Σ_matchings M z^|M| (product_e∈M w_e) |Ω_M>.

Every term is an even-triplet SU(2) singlet. This is a finite polynomial through |M|=16, not a bosonic exponential approximation. It is nonzero because its vacuum coefficient is one. Negative z is required at first order: ψ_ground=|0>-(g/4)C†|0>+O(g²).

Only matchings with the same occupied support overlap. Their union is a collection of alternating loops, including doubled-edge loops. The contraction is 3 per loop because J²=I. Thus

  Z=<ψ,ψ>=Σ_{M,M':supp M=supp M'} z^(2|M|) w(M)w(M') 3^loops(M,M').

There is no orientation sign on a pair. Spherical component signs must nevertheless be retained in physical local actions. On length-two periodic directions use w=2 and all its cross products; treating the two copies as independently occupiable dimers is wrong. For unequal real pair amplitudes replace z w_e by a_e; the overlap products can then have signs.

## 2. An exact missing-sector residual bound

The 8x4 graph is bipartite. Every occupied configuration of ψ has equally many triplets on A and B. Hence ψ has no q=2 same-sublattice component. In that component of (H'-rho)ψ, Q and rho vanish, annihilation of ψ_4 still leaves balanced A/B occupation, and creation from vacuum gives an A/B pair. Only hopping D acting on ψ_2 contributes.

Let n_uv=Σ_k w_uk w_kv for distinct same-sublattice sites u,v. Hopping either endpoint of an initial pair gives

  [D C†|0>]_{u,v}=2 n_uv Ω_uv,
  [(H'-rho)ψ]_{u,v}=g z n_uv Ω_uv.

Distinct two-site supports are orthogonal. Therefore, for EVERY real rho (and in particular the exact Rayleigh quotient),

  ||(H'-rho)ψ||²/Z >= 3g²z² Σ_{unordered same-sublattice u,v} n_uv² / Z.

Geometry-only enumeration gives 32 pairs with n=1 and 80 with n=2, hence Σ n²=352 and the coefficient is 1056. The 80 consist of 64 diagonal pairs and 16 opposite-y pairs; the latter have two length-two paths because circumference is four. The remaining 128 same-sublattice pairs have n=0.

A rigorous norm upper bound is available without a transfer contraction. At fixed support with k occupied A sites and k occupied B sites, let S be the weighted number of matchings. Since weighted degree is four, S<=4^k. Since loops<=k, the contribution is <=z^(2k)3^k S² <=(12z²)^k S. Sum over first matchings and bound choices at each of the N/2 A sites independently, ignoring exclusion of repeated B destinations:

  Z <= Σ_M (12z²)^|M| w(M) <= (1+48z²)^(N/2).

This also holds for aggregated positive multiedges of weighted degree four. For N=32, g=11/100, z=-11/400, it yields Z<=1.769163498803 and

  variance >= 1056g²z²/(1+48z²)^16 = .00546193724126837... .

Exact rational values are in geometry.json. In the perturbative scaling z=-g/4+O(g²), the unavoidable variance begins at 66g⁴+O(g⁵), whereas the disconnected q4 coefficient is correct: z²(C†)²/2=g²(C†)²/32+O(g³). Thus curing disconnected higher q does not cure the leading omitted connected pair motion. A generic claim that the norm is near one is unnecessary and has not been used.

## 3. Exact finite-torus contractions: formal representation versus cost

The matching state is a PEPS of edge bond dimension 4 (unused, or one of three triplet colors). A local tensor permits either all unused legs with physical singlet, or exactly one occupied leg with its physical triplet. Put z w_e and J on edge tensors; avoid square roots by assigning the whole scalar to one endpoint/edge tensor. This gives exact rational tensors for rational z in the spherical convention. Physical local dimension is four.

The norm has bond dimension 16 on each edge. A column cut through W=4 edges has boundary dimension 16^4=65,536. Let T be the exact single-column double-layer transfer, including the periodic vertical closure. Then Z=trace(T^8). This trace is NOT evaluation of T^8 on one boundary vector. Dense T has 2^32 entries, already 32 GiB in binary64, before exact arithmetic. Multiplication or diagonalization of this matrix is not authorized and is not a plausible small computation. Propagating one basis boundary at a time reduces memory, but introduces up to 65,536 propagations, with no claim that sparse powers remain sparse.

A color-free loop-connectivity transfer can exploit the weight 3 per closed component. For a torus cut open into a strip, both the initial seam and the moving frontier must be retained until their periodic closures are made. At column boundaries there can be 8 original cut edges, hence 16 bra/ket endpoints. The unconstrained upper number of partial pairings is the telephone number T16=46,206,736. At intermediate vertex cuts in a column ordering there can be 10 cut edges and 20 endpoints, for the much looser upper T20=23,758,664,096. These are safe representation ceilings, NOT reachable-state counts, memory estimates, or measured run times. Planarity and compatibility should reduce them drastically, but torus seam closure cannot be omitted, and no Catalan-only planar bound is asserted. Even the smaller ceiling would exceed 256 MiB at eight bytes per state; exact weights and dictionary metadata cost more.

For a fixed width one can enumerate a finite transfer; the dependence is exponential/combinatorial in width. This is not a polynomial-time claim in general two-dimensional size. An exact reachable-connectivity counter, with all seams and closures, is the appropriate next cost calculation before any full 8x4 physical scalar evaluation.

## 4. Complete first and second moments

Use the local rung total and difference spins T_i=S_i1+S_i2 and R_i=S_i1-S_i2. Exactly A_ij=T_i·T_j+R_i·R_j. Thus H' is 32 onsite Q_i terms plus 64 edge terms h_e=(g/2)(T_i·T_j+R_i·R_j), with weighted multiplicities when required. Every moment can be obtained by finite tensor insertions in the same doubled network.

On a translationally invariant 8x4 ansatz, classify local terms by a=onsite,x-edge,y-edge. There are three mean insertions and, for H'^2, 9*32=288 ORDERED type/displacement insertions:

  <H'^2> = N Σ_{a,b,r} <h_a(0) h_b(r)>.

Include overlapping terms with their correct operator order, all nonoverlapping separations, and coincident terms; do not replace this by the square of a projected Hamiltonian. Expanding each edge into its six Cartesian product operators gives a conservative 32*(1+6+6)^2=5408 product-operator insertion contractions, before exploiting adjoints, symmetry, or shared environments. This is an exact count of this naive recipe, not the optimum cost. Complex intermediate Cartesian matrices may be avoided by spherical or invariant-delta tensors. Overlapping insertions multiply onsite matrices in the displayed order. Direct contraction of the residual norm is another implementation of the same full quantity.

Rational z and g allow exact rational contractions; fixed denominators can be factored and arbitrary-precision integer sums used. Finite-precision contraction without certified outward error is not a certificate. The complete H² and the accepted r1/r2 sector-count obligations must both be checked before a new Temple lower endpoint. A better trial alone proves no gap.

## 5. Minimal dressings and their inflation

A. Range-two exponential. Ordinary perturbation theory with vacuum coefficient fixed to one gives the q2 correction g² D C†|0>/16. Hence add pair coefficient g² n_uv/8 on same-sublattice distance-two pairs. An NN scalar shift also handles the D same-edge contribution; distance-two correction cannot be represented by changing z alone. A few parameters can distinguish axial and diagonal paths, respecting the special circumference-four multiplicity.

Including all axial-distance-two and diagonal pairs raises the number of edges crossing one intercolumn cut from four to twenty: 4 NN horizontal, 8 diagonals, and 8 length-two horizontal edges crossing from either of two source columns. The naive doubled edge boundary becomes 16^20. A better vertex-frontier representation retains two columns rather than one, but the periodic seam then doubles that memory too: potentially 32 bra/ket endpoints, with unconstrained partial-pairing ceiling T32=22,481,059,424,730,751,232. These huge ceilings are reasons to demand exact reachable-state counts, not proofs that every specialized algorithm is infeasible.

B. Full 14-orbit exponential. The accepted rectangular pair-orbit basis covers all 496 unordered pairs of 32 sites. Exponentiating a general fitted pair kernel therefore gives a dense pair graph, not a local width-four PEPS. A half-system cut can cross 256 pair edges; the physical Schmidt-rank bound 4^16 is already smaller than the naive virtual bound. No efficient rigorous full norm/H² method is supplied for that general state.

C. One marked correction. Prefer testing ψ=exp(zC†)(1+B†)|0>, where B† is the accepted q2 pair kernel minus zC† (after scaling the accepted vacuum coefficient to one). This fits q2 exactly while adding a controlled disconnected completion, and remains an even singlet. In each ket matching at most one edge is marked as B. Norm and H² need at most one marked edge in each layer, including their interference. This does NOT exponentiate the dense pair graph, and does NOT include disconnected products of two B edges.

An algebraic MPO for a general pair creator in a fixed site ordering needs states for no insertion, completed insertion, and three colors times open first-site identities; a simple upper bond dimension is 2+3N=98. Better cut-specific ranks can reduce it. Multiplying this MPO into the periodic-column MPS below gives a formal ket-bond inflation <=98, doubled-layer <=9604, before compression. Naively summing marked edges separately costs (1+496)^2=247,009 bra/ket terms per observable; translation and shared environments can reduce this, but neither reduction has been implemented. Restricting B to range-two orbits is the smaller first test. A full q<=6 polynomial corrector is more expensive still and needs a separate insertion-count proof.

## 6. MPS/PEPS comparison and bounded next experiment

The NN matching PEPS has D=4 but its column-grouped periodic MPS has ket bond chi=4^4=256 and column physical dimension 4^4=256. Its doubled transfer is the 65,536-dimensional object above. Opening the periodic MPS in the x direction can square the ket bond to 65,536. An open-cylinder contraction would be cheaper but computes the wrong physical trial geometry if periodic closures are dropped. An explicitly open-boundary MPS can still be a legal trial for the periodic Hamiltonian, provided all wrap Hamiltonian terms are retained; it is a different ansatz.

A separately optimized small open MPS could be easier to contract, but must be an exact even SU(2) singlet to reuse r2. The smallest nontrivial scalar-plus-vector virtual space has dimension 1+3=4; this is a representation possibility, not evidence that chi=4 is accurate enough. For the 8x4 snake ordering at most ten physical graph edges cross a cut, so a straightforward Hamiltonian MPO has bond <=2+6*10=62. Applying it to a chi-dimensional MPS and taking the full norm computes complete H² with enlarged bond <=62chi; generic dense costs can still be large. Benchmark sparse exact contraction and rational coefficient sizes rather than assuming cubic scaling at the original chi. An unconstrained floating MPS with broken SU(2) cannot simply inherit the even-singlet cutoff.

Recommended bounded fixture, only after approval if physical fixture work is desired:

1. Independently build the 4x2 weighted graph and spin-derived local Hamiltonian. Its full rung Hilbert dimension is 4^8=65,536. Aggregate vertical w=2 first.
2. At several rational z (including negative z and zero), compare an explicit small physical vector with the matching/loop and tensor constructions. Check norm, <H'>, COMPLETE <H'^2>, and residual by two independent routes. Check the geometry prediction 432 g²z²/Z for its same-sublattice q2 residual.
3. Repeat with a rational signed one-marked range-two pair correction. Check interference, doubled periodic bonds, both torus closures, and coincident H² insertions. Optional full14-orbit dressing is not a 4x2 object; use that geometry's actual pair-orbit set.
4. Separately run a STATE-COUNT-ONLY 8x4 connectivity pass under one CPU6, 60 CPU seconds, 256 MiB. No amplitude/Hamiltonian contraction. Record reachable states at every cut, transitions, seam sectors, temporary peak, and exact-counter storage. Abort before memory exhaustion. Prove completeness of the counter against 4x2 exhaustive fixtures.
5. Before a production proposal, include all 288 ordered H² insertion types (or prove an equivalent fused algorithm), marked-edge flags, arithmetic word growth, measured per-transition cost, and conservative total memory/time. If the counter fails the budget, stop this route instead of interpreting D=4 as permission to launch.

Given the exact missing-sector obstruction and unsettled torus cost, this is a lower-priority alternative to a directly measured new residual direction. No claim that the repaired pair ansatz reaches the approximately .000274 required endpoint improvement is made.
