# Exact local relative bound for the spin-1/2 bilayer

Take two rungs, spins (0,1) and (2,3), with unit rung gap. Let h_i=S_0·S_1+3/4 and h_j=S_2·S_3+3/4, and v=S_0·S_2+S_1·S_3. The eigenvalues of a(h_i+h_j)+g v are

- 2a+g/2, multiplicity 5
- 2a−g/2, multiplicity 3
- a+g/2, multiplicity 3
- a−g/2, multiplicity 3
- a−g/2 ± sqrt(a²−ag+g²), multiplicity 1 each.

An independent symbolic characteristic polynomial in the 16-dimensional physical spin product basis verifies this list. For g≥0 and a≥g/2, a valid lower bound is −b with

b=sqrt(a²−ag+g²)−a+g/2.

A rational upper enclosure of b yields an exact local positive-semidefinite certificate without a repeated matrix inertia calculation. Summing over the square-rung graph, with degree four and 2N edges counting periodic multiplicities, gives

H−E00 ≥ (1−4a)(H0−E00)−2Nb.

For a<1/4 the ordered unperturbed excitation bins retain their order. The first-excited-bin lower bound relative to E00 is 1−4a−2Nb. For N>2 its unconstrained optimum over a is

a*=g/2+sqrt(3)g(N−2)/(4sqrt(N−1)),

and the optimum is

1−2g−2g sqrt(3(N−1)).

Use this optimum only when a*<1/4. Otherwise enforce the required parameter constraint. Optimizing a full heat-tail enclosure is a different objective and may select a different a.

Independent exact numerical check for g=1/50, a=17/400, b=2163649829/500000000000: all sixteen rational leading principal minors are strictly positive. Code and exact values are saved beside this note.
