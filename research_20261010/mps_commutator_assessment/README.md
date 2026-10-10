# Low-cost assessment of a current-augmented excited MPS

Updated 2026-10-10 17:39 EDT / 21:39 UTC.

The exact local current identity and tiny two-vector fixtures pass. At n6,
an explicitly saved rational combination improves the trial excitation
energy relative to the fixed psi from0.769079740737225 to0.7205939266054274.
At n2 and n4 the two vectors are exactly dependent. These are finite trial
Rayleigh results, not physical eigenvalues or large-n predictions.

No n24 current contraction has been started. The straightforward route is
projected at about1,780 CPU seconds, exceeding the600-second gate. It therefore
fails the required low-cost screen. A carefully fused range-two source
automaton could reuse work, but its runtime and memory have not been measured;
it needs a separate small benchmark before any large run.

## Exact identity and local tensor

Let R_j=S_j^+/sqrt2, L_j=R_j adjoint, M_j=Sz_j. In the orthonormal spin-z
basis, h_j=M_j M_(j+1)+R_j L_(j+1)+L_j R_(j+1). Direct integer commutators give

    [h_j,R_j]=J_j=R_j M_(j+1)-M_j R_(j+1),
    [h_j,R_(j+1)]=-J_j.

For z^n=1 and A_q=sum_j z^j R_j,

    [H,A_q]=(1-z) sum_j z^j J_j.

At pi, z=-1 and the factor is2. If B_s=A_(s-1), B_-1=0, the physical
two-site word tensor for J is exactly

    Gamma_st=m_t B_s A_t-m_s A_s B_t.

`current_two_site_tensors.json` saves all nine integer26-square word tensors.
The verifier compares every tensor directly with the physical9-square J
operator applied to the corresponding MPS words.

For each n2,4,6, the verifier constructs the exact tiny physical state,
v=A_pi psi, and w=[H,A_pi]psi in two independent ways: full H applications
and the explicit current sum. It checks exact equality, momentum pi, Sz1,
and annihilation by total raising. No assumption that psi is an H eigenvector
is used. The2-square Gram and H-form matrices are saved in `tiny_results.json`.

At n6 the Gram determinant is positive. The generalized minimum is enclosed
using the exact quadratic discriminant and160-bit radical bounds. A rational
mixing coefficient with denominator10^9 produces a bona fide fixed trial
state whose exact Rayleigh quotient is saved. Its improvement is certified
directly, without treating a compressed eigenvalue as a physical spectral
bound. The two-vector span may again be completed into spin components by
the already proved singlet/highest-weight algebra, if its large-n inputs are
eventually contracted.

## Size, cost, and next bounded step

One explicit representation of the open-chain current sum uses four source
channels, giving bond4D=104. Two explicit periodic wrapping product terms
add2D. This supplies a safe periodic bound6D=156 for one current vector;
it is not asserted optimal. The proposed linear trial span still has at most
two vectors at one momentum. No new physical support beyond n6 was generated.

A direct reuse of the measured fixed-source engine would need up to24 mixed
displacements with two monomials each, plus13 current-current displacements
with four monomials each:100 contractions. At the measured mean of
231.4436/13 CPU seconds this is about1,780.34 CPU seconds, before extra source
building. Sequential peak memory would remain modest, but time exceeds the
600-second budget. Nearest momenta are therefore not attempted either.

The bounded next implementation is a fused source automaton for one-site /
two-site mixed sources and the accumulated H insertion, explicitly including
periodic-wrap paths. It should first reproduce the saved n2/4/6 fixtures and
measure resource growth on one moderate auxiliary contraction. No claim is
made that this unimplemented optimization fits the large-n gate.

Run `python verify_tiny_commutator.py` in a disposable sibling copy to
reproduce this assessment. It takes under one CPU second and about23MiB.
The code pins one CPU and imposes700MiB address-space /600 CPU-second limits.
The archived witness deliverable and all its staged review inputs remain
unchanged.
