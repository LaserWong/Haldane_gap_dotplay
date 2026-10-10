# Exact finite-length singlet completion to70 compact witnesses

This argument concerns only the fixed archived state at n=24 whose exact
displacement contractions have been saved. It does not assume an exact
SU(2) property of the tensors at arbitrary length or an H eigenvector property.

Write R=S_total^+/sqrt2, L=S_total^-/sqrt2, and M=Sz_total. On each physical
spin the normalized raising and lowering matrices have unit nonzero entries.
They satisfy [R,L]=M, [M,R]=R. Direct integer two-site commutators verify
[H,R]=[H,L]=[H,M]=0 for the periodic Heisenberg Hamiltonian.

The checked tensor charge selection gives M psi=0. The exact circulant Gram
data give

    ||R psi||^2=n sum_r C(r)=0.

Thus R psi=0. Also

    ||L psi||^2=<psi,RL psi>=<psi,(LR+M)psi>=0,

so L psi=0. Equivalently, the physical Casimir annihilates psi; it is a
singlet at this finite length. This is a consequence of exact zero norm,
not an assumed rounded or approximate symmetry.

For every local tangent v_j=R_j psi, global R commutes with R_j. Therefore
R v_j=0 and M v_j=v_j. The normalized ladder identity gives RL v_j=v_j.
For all sitesi,j, regardless of whether v_j is an H eigenvector,

    <L v_i,L v_j>=<v_i,RL v_j>=<v_i,v_j>,
    <L v_i,H L v_j>=<v_i,H RL v_j>=<v_i,H v_j>.

Moreover,

    L v_j=[L,R_j]psi=-Sz_j psi.

Consequently the complete longitudinal Gram and H-form matrices equal the
already contracted transverse matrices. Every nonzero Fourier mode acquires
an exactly orthogonal Sz0 partner with the identical norm and Rayleigh value.
The new state is a single longitudinal source, so its MPS bond dimension is
at most52; there is no increase to104.

The global spin flip supplies the Sz-1 partner as before. All23 nonzero
momenta have certified positive norm. Their three components and psi give
1+3*23=70 orthogonal denominator trial states. The exact zero q0 mode is
excluded in every component. Distinct momenta are orthogonal because they
have distinct eigenvalues of the unitary translation, and distinct Sz sectors
are orthogonal independently. psi has momentum0 and Sz0.

The verifier also builds full n2,4,6 physical coefficient vectors. At every
site it checks exact vanishing of total raising/lowering on psi, equality
L v_j=-Sz_j psi, raising back to v_j, and equality of all displacement Gram
and complete H forms. The large-length inference itself relies only on the
saved exact n24 zero norm and checked local spin algebra.

The70-state trace lower bound uses multiplicity6 for momentum representatives
k1,...,11 and multiplicity3 at k12. Its exact scalar replay is separate from
the frozen48-state result. It retains all original caveats: these are trial
Rayleigh contributions, not physical eigenvalue or degeneracy claims, and
an inconclusive lower-trace screen supplies no denominator upper certificate.
