# Independent longitudinal fourth-witness review

This extension is separate from the immutable three-state review in the parent directory. It uses the same uniform periodic spin-1 Hamiltonian, unit coupling, even lengths, physical basis (-1,0,+1), and periodic multibond convention at n=2. Its inherited fixed-recipe limitations are exactly those explained in the core REVIEW.md.

## Fourth vector and orthogonality

Define Φz = sum_j (-1)^j Sz_j ψ_n. Its local source tensor is B_m=m A_m. Each source preserves total Sz, so Φz lies in Sz=0. For even n, cyclicity of the MPS trace gives Tψ=ψ, whereas translation of the alternating source sum gives TΦz=−Φz. Since T is unitary, <ψ,Φz>=−<ψ,Φz>=0. It is orthogonal to Φ± because their Sz charges are ±1. Strictly positive exact norms make these four vectors linearly independent.

No exact SU(2) symmetry of the chosen MPS is assumed. Exact finite-length contraction proves that Φz has the same norm and Hamiltonian numerator as the chosen rationally scaled Φ+ at every even n≤24. This equality is a checked arithmetic result in the relevant finite sizes, not an inferred spin-multiplet statement. For example, n=4 longitudinal support has 10 configurations while the transverse vector has 16; the fourth vector is not a duplicate physical state.

The tangent MPS bond bound is at most 52, using triangular tensors and the fixed off-diagonal closing matrix. The denominator retained span dimension is four, with physical Hilbert dimension 3^n; the numerator retains one state at length 2n in full dimension 3^(2n). Auxiliary charge blocks remain separate from these physical and linear-span dimensions.

## Independent replay

The local review builder enumerates all norm and Hamiltonian bond source placements from physical Sz and h matrices. Both source charge shifts are zero. The exact source file is compared entry by entry; its ground components reproduce the inherited block file byte for byte. The direct fixtures expand every word at n=2,4,6 and explicitly test zero ψ overlap, translation eigenvalue −1, norms, full-H numerators, and support sizes.

A separate global-index GMP engine with zero source charge shifts contracts every even n≤24. It is independent of the producer's rectangular charge-block representation. Every norm and full-H numerator is compared with the frozen longitudinal outputs and the independently reviewed transverse outputs. No physical support above n=6 is constructed, and no eigensolver is used.

## Four-state scalar obstruction

At the relevant sizes the independently verified αz=α1 gives the stronger Jensen lower bound

Z_n(β) ≥ exp(-βα0) [1+3 exp(-βg)],  g=α1−α0.

Consequently the chosen fixed one-Rayleigh numerator recipe obeys

J ≤ exp(-2βδ)/[1+3 exp(-βg)]^4,
C ≤ exp(-2βδ)/[1+3 exp(-2βg)]²,

with δ=R−2α0. The complete hot/closed-box/cold covering, directed exponential enclosures, monotone G replay, all whole-cycle time-first delays, and treatment of inconclusive caps are independently repeated as in the core. The new necessary-condition bounds still exclude n=14,16,20 for every β≥0. At n=24 only the closed-box union [31/4,11] remains inconclusive. Its width is 13/4, compared with 19/4 for the three-state screen. A smaller unresolved interval does not assert existence of a successful certified seed.

## Hypothetical trace-budget calculation and its contradiction

At n=24 and β=8, suppose both required upper denominator traces were at most 201/200 times the three-state lower trial trace at their respective temperatures. A downward-rounded replay of that explicitly hypothetical assumption reaches a common scalar lower endpoint greater than 99/100, after two additional time-first cycles and the specified canonical conversion. This is a conditional algebra calculation only.

The fourth orthogonal witness proves the premise impossible already at β=8:

Z_24(8)/trial3(8) ≥ trial4(8)/trial3(8)
= [1+3 exp(-8g)]/[1+2 exp(-8g)] > 1.0189342 > 201/200.

Independent exact enclosures verify both the conditional replay and this contradiction. Therefore the apparent 0.5% tail allowance above an incomplete three-state trace cannot be advertised as a feasible denominator accuracy target. It provides no trace upper certificate or Haldane gap conclusion.

All numerical displays are subordinate to the exact rational outputs. RESOURCES.json gives the actual final replay costs and memory. The extension's own MANIFEST_SHA256.json and SEAL.json cover only this extension; the parent core remains unchanged.
