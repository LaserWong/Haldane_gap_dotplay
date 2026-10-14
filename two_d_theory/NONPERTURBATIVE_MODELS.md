# A nonperturbative two-dimensional example with a one-vector trial space

October 10, 2026.
The fully frustrated spin-1/2 bilayer provides a directly reproducible example based on exact conservation of the total spin on each rung.
The argument uses no coupling expansion.
Its one-dimensional trial space follows from this exact structure and does not imply a comparable trial-space size for general strongly coupled models.

## 1. Fully frustrated and ordinary bilayers

Each square-lattice cell contains two spin-1/2 degrees of freedom.
Define

$$
P_r=\mathbf S_{r,1}\cdot\mathbf S_{r,2}+\frac34 I,
\quad \mathbf T_r=\mathbf S_{r,1}+\mathbf S_{r,2},
\quad Q=\sum_rP_r.
$$

Here P_r is the triplet projector and T_r²=2P_r.
We take

$$
H_J=Q+J\sum_{\langle r,s\rangle}\mathbf T_r\cdot\mathbf T_s.
$$

Every intercell edge contains four Heisenberg couplings of strength J, comprising two intralayer bonds and two crossed interlayer bonds.
The ordinary bilayer contains only the intralayer bonds.
Thus J=0.3 here and g=0.01 or 0.02 in the ordinary-bilayer heat-trace certificates refer to different Hamiltonians.
They cannot be compared as a direct extension of one model's certified parameter interval.

The fully frustrated bilayer and its local total-spin conservation are established model structures.
A primary source is J. Stapmanns et al., Physical Review Letters 121, 127201 (2018), Eq. (2), available in the authors' full-text archive and as arXiv:1805.11017.
The inequalities and small-system conventions below are derived independently here.
The numerical transition point in that paper is not used as a rigorous gap proof.

## 2. Exact one-dimensional trial space

Every P_r commutes with H_J.
The product |Ω⟩ of rung singlets satisfies

$$
P_r|\Omega\rangle=0,
\quad \mathbf T_r|\Omega\rangle=0,
\quad H_J|\Omega\rangle=0.
$$

The trial space span{|Ω⟩} therefore has dimension one, with energy and full residual exactly equal to zero at every volume.
This vector has 2^N nonzero coefficients in the physical-spin S^z product basis, but it is a single basis vector in the rung singlet–triplet basis.
Representation size, number of retained trial vectors, and full excited-space dimension are distinct quantities.

In a sector with q triplets, the Hamiltonian is an interacting spin-1 model on the occupied-cell graph, with dimension 3^q.
Adjacent Heisenberg terms on that graph generally do not commute.
The full excitation problem has therefore not been reduced to one dimension.

## 3. Uniform bound from a star operator

First consider periodic rectangles with both side lengths at least 3, so every cell has four distinct neighbors.
In the sector P_r=1, the central total spin is 1 and the four neighboring cells have total spin S≤4.
Angular-momentum addition gives

$$
\mathbf T_r\cdot\sum_{s\sim r}\mathbf T_s\ge-5P_r.
$$

For S≥1 the lowest eigenvalue is −(S+1), while S=0 gives zero.
Summing the star inequalities counts each edge twice and yields

$$
H_J\ge\left(1-\frac52J\right)Q.
$$

For 0≤J<2/5, every such finite volume has a unique singlet-product ground state and a uniform gap of at least 1−5J/2.
This sufficient interval follows from an exact angular-momentum bound rather than a perturbation series.
It does not identify the physical phase boundary.

### Exact gap at J=3/10

For q≥4, the preceding bound gives E≥q/4≥1.
The q=1 sector has energy exactly 1.
For q=2, there is at most one occupied edge, so E≥2−2J=1.4.
For q=3, the simple graph has at most three edges and each satisfies T_r·T_s≥−2, giving E≥3−6J=1.2.
Thus every periodic rectangle with both side lengths at least 3, including every integer square L≥3, has

$$
\Delta=1\quad\text{at }J=3/10.
$$

An isolated triplet attains this energy.
The same argument establishes the exact gap throughout 0≤J≤3/10.

## 4. Repeated bonds at length 2

The exact thermal transfer representation requires two adjacency terms in a periodic direction of length 2.
The 2×2 cell graph is consequently a four-cycle with doubled edges.
Group its opposite vertices into A and B to obtain

$$
H_J=Q+2J\mathbf T_A\cdot\mathbf T_B.
$$

If the groups contain q_A and q_B triplets, their total spins are at most q_A and q_B.
The largest antiferromagnetic energy reduction is

$$
2J\min(q_A,q_B)\,[\max(q_A,q_B)+1].
$$

Enumeration over q_A,q_B∈{0,1,2} gives the lowest energy among nonempty sectors,

$$
\Delta_{2,2}
=\min\{1,\,2-4J,\,3-6J,\,4-12J\},
\quad 0\le J<1/3.
$$

At J=3/10, this gap is 2/5.
Together with the preceding result, it gives an exact gap infimum of 2/5 over all integer squares L≥2, while every square L≥3 has gap 1.

At J=1/3, a singlet in the all-triplet sector of the 2×2 system becomes degenerate with |Ω⟩.
A model family that includes this L=2 multigraph and requires a unique singlet ground state must therefore end its allowed J interval before 1/3.
This finite-volume restriction differs from the physical transition on the infinite plane.

## 5. Spectral tails for all seed geometries

A plaquette bound gives a simple estimate uniform over the required rectangles.
For a four-cycle, let T_A and T_B be the total spins on opposite pairs of vertices.
Its four edge terms sum to K=T_A·T_B.
Angular-momentum enumeration over all singlet/triplet occupations gives

$$
K\ge-\frac32\sum_{r\in\square}P_r.
$$

Summing periodic plaquettes counts each edge twice and each cell four times, so

$$
H_J\ge(1-3J)Q.
$$

This inequality includes the repeated-bond convention at length 2.
All seed rectangles at J=3/10 can therefore use γ=1/10.
If both sides are at least 3, the star bound improves this to γ=1/4.

The total dimension of the q-triplet sector is binom(N,q)3^q and its energy is at least γq.
The entire omitted spectrum is thus covered by the binomial bound

$$
1\le Z_N(\beta)\le\sum_{q=0}^N\binom Nq3^qe^{-\beta\gamma q}
=(1+3e^{-\beta\gamma})^N.
$$

This estimate requires no full many-body diagonalization.
It retains all omitted degeneracies and uses an exact zero-residual trial state.

## 6. Three-purity certificate

Joint time reversal on a rung squares to +1, allowing a real structure with T_r=iA_r.
The identical-factor real tensor expansion of −J T_r·T_s then satisfies the selfadjoint thermal-transfer conditions of `THEORY.md` in both directions.
For z=1+3e^{-βγ} and N=nm,

$$
A\ge z^{-2N},\quad B\ge z^{-4N},\quad C\ge z^{-8N}.
$$

With n=m=2, β=120, and γ=1/10, the rational lower bounds lie directly in the small-defect regime of the three-purity theorem.
They give the bootstrap bound

$$
\Delta_L\ge0.033085166891
$$

for every integer square L≥2.
The largest seed geometry contains 16 rungs and 32 physical spins, with full Hilbert-space dimension 4,294,967,296.
Only one exact trial vector is retained.

Using n=m=4, β=80, and γ=1/4 gives the bootstrap lower bound 0.132295274293 for L≥4.
The largest seed now contains 128 physical spins, but the tail remains a binomial expression.

The direct local inequalities already give a stronger gap for this model.
The thermal calculation establishes that the same three-purity framework can accept a noncommuting example without a coupling expansion and with a very small exact spectral input.
It does not improve on the direct angular-momentum proof for this special model.
The script `fully_frustrated_bilayer.py` and the two `fully_frustrated_one_trial_n*.json` files provide fully rational recomputation.

## 7. Sensitivity to broken local conservation

The numerical test convention uses intralayer coupling J+ε and crossed coupling J.
For D_r=S_(r,1)−S_(r,2), the edge interaction becomes

$$
\left(J+\frac\epsilon2\right)\mathbf T_r\cdot\mathbf T_s
+\frac\epsilon2\mathbf D_r\cdot\mathbf D_s.
$$

The second term can create a pair of triplets from two singlets and breaks conservation of the local P_r.
The one-dimensional ground-state trial space generally has a nonzero residual when ε≠0.
A sensitivity test must therefore report the full residual, the certified heat-trace interval, and the required support size as ε increases.
The exact one-vector result at ε=0 does not extend without these checks.

The transfer conditions can still be examined in both directions.
The layer-index coupling matrix has eigenvalues 2J+ε and ε.
For ε≥0, its decomposition into T and D channels has nonnegative coefficients and identical factors.
The chosen small positive-ε tests therefore preserve the transfer structure.

## 8. Other structured candidates

AKLT/MPS parent Hamiltonians have finite-dimensional virtual representations.
Fixed bond dimension does not imply finite support in the S^z basis or a certificate for the entire positive spectrum using one or two ordinary vectors.
Frustration-free finite-size criteria or local positive-operator decompositions are often more suitable for these models.

Shastry–Sutherland-type orthogonal dimers also have intervals with exact singlet-product ground states and are candidates for further structural compression.
Their thermal spectral tails and selfadjoint transfers in both directions would need separate proofs.
The completed nonperturbative certificate here concerns the explicitly defined fully frustrated bilayer.

Two primary sources for further examination are B. S. Shastry and B. Sutherland, “Exact ground state of a quantum mechanical antiferromagnet,” Physica B+C 108, 1069–1070 (1981), in the author's archive, and V. Karimipour and L. Memarzadeh, “Matrix product representations for all valence bond states,” Physical Review B 77, 094416 (2008), at the journal.
The full PDF of the former could not be retrieved during the original research.
Search results supported its triangle decomposition and exact dimer ground-state construction, but unread details were not used to establish a new Shastry–Sutherland numerical certificate.

## 9. Independent small-system diagnostics

Independent numerical checks on the 2×2 rung torus at J=0.3 confirmed a unique ground state, zero residual for the exact product state, and a floating-point gap of 0.4.
For the 4×2 rectangle, a full calculation resolved by occupation number and S^z gave gap 0.8.
Its physical Hilbert space has dimension 65,536 and its largest dense block has dimension 1,107.
Further 2×2 checks found ground-state degeneracy 2 at J=1/3 and showed that the original singlet product is no longer a ground state at J=0.35.

The independent numerical directory stores these floating-point spectra and the local star and plaquette matrix checks.
They diagnose the analytic construction.
The proof rests on the angular-momentum inequalities and rational heat-trace tails above.
No full physical-spectrum diagonalization was performed for the 4×4 rung system.
