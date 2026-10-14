# A positive-gap model that cannot enter a unique-ground-state purity bootstrap

## Scope and normalization

Let G be a finite connected undirected weighted multigraph on n ≥ 2 vertices.
Every edge occurrence has a strictly positive rational weight J_e; repeated
and reverse-listed edges are counted separately. There are no self-loops.
On the full spin-half Hilbert space, take

H = −Σ_e J_e S_i^z S_j^z, with S_i^z eigenvalues ±1/2.

No symmetry sector is selected. The gap below means the energy from the
entire ground eigenspace to the next distinct eigenvalue. It does not mean
the difference of the first two eigenvalues counted with multiplicity.

## Exact finite-graph spectrum identity

Represent a computational configuration by signs σ_i ∈ {−1,+1}. Let S be
the sites of sign −1 and c(S) the total weight of edges crossing from S to
its complement. Direct substitution, edge by edge, gives

E(S) = E_0 + c(S)/2,    E_0 = −Σ_e J_e/4.

Connectedness and positive weights imply c(S)=0 precisely for S=∅ or V.
Thus the ground degeneracy is exactly two, and

g(G) = (1/2) min_{∅≠S⊊V} c(S) > 0.

This is an exact equality, not a variational bound. The two aligned
configurations span the ground space. A cut attaining the minimum gives
an actual excited eigenstate. Disconnected inputs are rejected rather
than applying the twofold-degeneracy formula outside its hypotheses.
With k connected components the degeneracy would instead be 2^k.

## Purity obstruction at every finite size

For β ≥ 0 define ρ_β=e^(−βH)/Z(β) and the temporal thermal purity
T(β)=Tr ρ_β²=Z(2β)/Z(β)². Global spin flip maps each configuration to a
different configuration of exactly the same energy. Label these pairs
by a and let p_a be their total Gibbs probability. The two eigenvalues
in pair a are p_a/2, hence

T(β) = (1/2) Σ_a p_a² ≤ (1/2)(Σ_a p_a)² = 1/2.

For every finite β and n≥2 the inequality is strict, because more than
one pair has positive probability. As β→∞ the single aligned pair
receives all probability and T(β)→1/2. This reasoning is exact and does
not depend on numerical resolution, retained eigenpairs, or tail bounds.

Any criterion requiring T ≥ θ with θ>1/2 can therefore never start on
these full-space finite models. In particular the dedicated thresholds
T ≥ 99/100 (d=1) or T ≥ 499/500 (d=2) cannot hold. The general adapter
also requires temporal purity near one. Enlarging any finite seed,
cooling further, or increasing numerical trial rank cannot change the
bound. A canonical staircase contains a temporal edge, so improving
spatial edges does not evade this obstruction. Failed recurrence or
resource limits need not be used as evidence: the analytic upper bound
already rules out the required entry condition at every possible
finite temporal basepoint.

This is a **method-specific impossibility**, accompanied by an exact
positive physical excitation gap for each input graph. It is neither a
proof of physical gaplessness nor an impossibility theorem for other
gap methods. A ground-space-aware criterion, domain-wall argument, or
appropriately justified symmetry-resolved analysis is the next research
step. Merely replacing T by 2T in the existing theorem is not justified:
its transfer and recurrence hypotheses must be proved again. Similarly,
a sector gap does not become a full-space gap without additional work.

## Finite versus uniform-family statements

The diagnostic computes one graph's exact cut. It makes no uniform-family
claim from a finite list of cuts: positive g(G_n) at every finite n alone
does not bound inf_n g(G_n) away from zero.

There is a simple all-size family where the bound can be proved directly.
For a periodic one-dimensional chain of length L≥2, include each positive-
direction edge (i,i+1 mod L) with common weight J>0. When L=2 there are
two parallel edges. Every nonconstant cyclic sign sequence has at least
two sign changes (changes alternate entering and leaving S), whereas a
contiguous nonempty proper interval has exactly two. Consequently the
minimum cut is 2J and g_L=J for **all** L≥2. This is a uniform positive
gap together with an all-finite-size purity obstruction. If L=2 instead
uses a simple graph convention its single-edge gap is J/2; conventions
cannot be silently exchanged.

The tests also examine small two- and three-dimensional periodic graphs
with the existing positive-direction multigraph convention. These are
finite validations only. No all-size higher-dimensional torus cut bound
is claimed here.

## Implementation and verification

`gapflow.ising.weighted_min_cut` uses exact Fraction arithmetic and the
Stoer–Wagner contraction algorithm. In each phase it grows a set by
maximum accumulated adjacency weight. The standard maximum-adjacency
phase lemma says that the last vertex defines a minimum cut separating
the last two selected vertices. Record its weight and contract those
two vertices; every cut that does not separate them survives contraction
with its weight unchanged. Therefore an optimal cut either appears as
an optimal separating cut in that phase or survives to the next phase.
The smallest recorded phase cut is the global minimum. Vertex groups
preserve an original-graph witness cut. Positive parallel edges are
summed before phases. Tie breaking is deterministic by vertex index.

Storage is O(n²+m), with O(n³) rational arithmetic operations; rational
bit complexity is additional. The diagnostic does not allocate a
2^n-dimensional basis or matrix. It is intended for bounded small and
moderate graphs, not an unbounded search or a promise of calibrated
wall time. Source weights must be exact integers, rational strings,
or Fraction instances; floats are rejected.

`diagnose_ising_obstruction` returns exact rational energies/cuts as
strings, the witness cut, ground degeneracy, purity upper bound and
limit, a threshold-dependent obstruction flag, and an explicit
recommendation to change criterion rather than grow the seed. A
threshold ≤1/2 is conservatively labeled not excluded by this upper
bound; it is not declared reachable or a valid alternative theorem.

`tests/test_ising.py` independently enumerates diagonal configuration
energies for 84 reproducibly generated connected rational-weight graphs
of 2–8 sites, additional cycles and finite tori, and parallel-edge
examples. It compares ground degeneracy, exact ground energy and exact
next-distinct-energy gap with the cut result, checks the returned cut
weight in the original graph, and crosschecks an independently built
`Model.exact_hamiltonian`. Finite-temperature numerical purity samples
are sanity checks only; the pair-probability proof establishes the
all-temperature bound. Invalid size, disconnected graph, self-edge,
invalid endpoint, nonpositive/inexact weight, and invalid threshold
inputs are rejected. No external package installation or remote write
is required.

Run: `python -m unittest discover -s tests -p test_ising.py -v`.
