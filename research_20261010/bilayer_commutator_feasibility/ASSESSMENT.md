# Feasibility of an enlarged denominator without q8 enumeration

2026-10-10 17:40 EDT / 21:40 UTC. Assessment and exact conditional residual budgets only. No production contraction, M6, or new denominator certificate has been generated here.

## Outcome

The commutator route addresses the missing q8 norm, and the remaining enlarged second-moment blocks can all be assembled with q2/q4/q6 data. An 8x4-only gated producer is promising and targets the diagnosed bottleneck. It must compute additional q4 and q6 norm contractions; obtaining only the commutator term is not enough.

Independent local hard-core identities and small physical fixtures are being provided separately in `../hardcore_pair_commutator`. The formulas below use its C† equal to the pair-creation part of A=2V, not a canonical-boson approximation.

## Full block accounting

Write H'=Q+tA, t=g/2. The even base families are B, L=A42 B_pair, R=A44 L, M=A64 L, Ufam=R+M. Here Q is triplet number and the symbol Ufam is a family, distinct from a spectral upper endpoint. Write C†=A_(q+2,q), C=(C†)*, and Dq=Aqq. Define

    P=D4 R+C M                 (q4),
    T=C† R+D6 M                (q6).

Then the complete image of the new family is

    H' Ufam = t C R + (4R+tP) + (6M+tT) + t C† M,

with orthogonal q2, q4, q6, q8 components. Every term is essential. Therefore

    J_UU = 16 V+36 W
           +t[8 X+10(Y+Y*)+12 Z]
           +t²[D2+P*P+T*T+Q8],

where the old exact matrices are V=R*R, W=M*M, X=R*D4R, Y=R*CM=(C†R)*M, Z=M*D6M. The new pieces are

    D2=(CR)*(CR)=S* G_pair^(-1) S,
    Q8=(C†M)*(C†M)=(CM)*(CM)+M*[C,C†]M.

Here S=L*R, and G_pair is the diagonal Gram on the complete pair-orbit basis. The formula for D2 follows from B_pair*CR=L*R and completeness of the translation-invariant singlet q2 family. It requires no extra contraction.

All mixed blocks J_(B,L),U are already determined: H'(B,L) lies entirely in span(B,L,Ufam), so use its exact known coordinate map and the enlarged first-moment matrix. Equivalently these are the existing base moments through M5. Only J_UU needs new information. One symmetric matrix

    K2=D2+P*P+T*T+(CM)*(CM)+M*[C,C†]M

is sufficient for new coupling-independent geometry, although its pieces should be saved separately for audit.

The commutator term can be negative. Q8 is nonnegative only after its sum with (CM)*(CM); neither dropping the commutator nor replacing it by a bosonic constant is justified.

## Required support coverage

- CM and P require ALL q4 supports containing the fixed origin, including supports on which L or R vanishes. Pulling CM from M on S union an empty geometric edge is local and uses only q6 source amplitudes.
- M*[C,C†]M needs only M-active q6 bra supports, as in the old exact-third-moment contraction.
- T*T requires MORE than those M-active supports. A64R or A66M may be nonzero where M vanishes. Stream all fixed-origin q6 supports, or prove a complete larger support filter. A filter requiring two geometric edges is unsafe for this term; at least one geometric edge suffices as a necessary support condition, but unrestricted fixed-origin enumeration is simplest for an 8x4 first run.
- Translation rescaling is N/4 for q4 bra expectations and N/6 for q6 bra expectations. Use the occupation sector of the contracted bra, not the unconstructed q8 output. In particular Q8 as a q6 operator expectation uses N/6 after the identity is applied.

Full-support and fixed-origin small fixtures must match before a larger run. The local hard-core action must preserve rung occupancy constraints and spin-index contraction signs.

## Size and memory budget, without launching a contraction

For 8x4, d=14 pair orbits. Existing q4 R cache has C(32,4)=35,960 entries, 6,041,280 bytes in the current implementation. Fixed-origin q4 has C(31,3)=4,495 supports. The old M-active q6 bra list has 73,206 supports. ALL fixed-origin q6 supports number C(31,5)=169,911, only 2.32 times the old list. Stream these with 15 matchings and 14 orbit coefficients; do not cache physical q6 states. No q8 matching basis is needed.

For 8x8, all fixed-origin q6 supports number C(63,5)=7,028,847, substantially larger than the 992,424 old active M bra supports. The old q4 cache is 106,743,168 bytes. Do not extrapolate old timings into an unconditional promise. Benchmark 8x4 first, and do not launch 8x8 until an explicit resource gate passes.

The old geometry timing was .645 s for 8x4 and 6.81 s for 8x8, but the new q6 norm and commutator loops cost more per support. These old timings are contextual, not runtime estimates for the new algorithm. Pin one CPU, BLAS1, 1 GiB; a 600 CPU-second/700 MiB projected gate would be conservative for any future producer. No such production job was started in this assessment.

## A quantitative acceptance target

Exact rational enlarged trial vectors were recomputed using the existing first-moment matrices only. Their means and conditional complete-variance budgets are saved in residual_budgets.json.

For 8x4:

- Enlarged Rayleigh rho = -.25305415013664406...
- Diagnostically useful candidate ground lower ell = -.2533447774532962...
- To certify this ell using the same sector cutoff a, it suffices that the COMPLETE exact variance satisfies

      v < (rho-ell)(a-rho) = .0004351875293320612...

This ell closes 75% of the old interval while leaving the original 4x4 denominator untouched; the earlier conditional scan then had 99 successful beta-grid proposals. The variance has not yet been computed, and no success is inferred. If the fixed vector misses this budget, a full enlarged moment-pencil optimization can still perform better than this single-vector Temple test; retain full matrices when inexpensive.

For 4x4, the analogous 75%-closure target requires variance below .0000692338896630712..., with enlarged mean -.12677706356575855.... Improving this patch alone was not enough in the diagnostic, so it is lower priority.

The ideal zero-variance endpoint is just the new mean and gives an optimistic ceiling on the benefit of this fixed vector. It is a conditional diagnostic, not an assumption that the enlarged family is invariant or its residual is zero.

## Recommended next bounded task

1. Adopt and independently check the separate exact local commutator proof and 4x2 physical q8 Gram fixture.
2. Implement q4 CM and P, q6 T, and M*K M contractions, saving separate matrices and integer overflow bounds.
3. Verify full vs fixed-origin results on 2x2/4x2, plus direct physical H'² on the enlarged family where feasible. Ensure T*T includes M-zero supports.
4. Run a representative small 8x4 microbenchmark only; project memory and time under the hard cap.
5. If the gate passes, compute ONLY 8x4 new geometry, verify positivity of Q8 and full J, then calculate the complete variance budget and/or enlarged ground pencil. Reuse unchanged 4x4 input first.
6. Only a successful exact scalar and all-size replay followed by independent review can promote a g=.10 result. No such result is presently claimed.

## Local-fixture evidence received

The independent local derivation reports exact 4x2 physical q8 Gram agreement for all five M columns. For coefficients c_i=(-1)^i(i+1), the q8 norm is 3,898,368 = 18,705,408 - 14,807,040; the commutator term is strictly negative. A saturated 3x2 fixture tests cancellation to zero. See the separately sealed hardcore_pair_commutator proof and test record; these are not production 8x4 residual data.
