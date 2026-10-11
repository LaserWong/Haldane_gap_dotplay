# Independent review: length-resolved finite bridges

2026-10-11 04:29 UTC / 2026-10-11 00:29 America/New_York (EDT).

## Final accepted statement

For every integer M ≥ 2, the periodic spin-one alternating Hamiltonian

    H_M(g) = Σ_(j=1)^M [S_(2j−1)·S_(2j) + g S_(2j)·S_(2j+1)],
    S_(2M+1) = S_1,

has a unique ground state and the following physical-unit gap lower bounds throughout the respective closed intervals:

- gap ≥ .020 for 9998709/10001291 ≤ g ≤ 10001291/9998709;
- gap ≥ .015 for 1249773/1250227 ≤ g ≤ 1250227/1249773;
- gap ≥ .010 for 9997841/10002159 ≤ g ≤ 10002159/9997841;
- gap ≥ .005 for 156213/156287 ≤ g ≤ 156287/156213.

The first bond coefficient is exactly one. There are L = 2M physical sites and full Hilbert dimension 3^(2M). The eta radii, with eta = (1−g)/(1+g), are respectively 1291/10000000, 227/1250000, 2159/10000000 and 37/156250. All endpoints are exact rationals. These are sufficient neighborhoods, not optimal widths, actual-gap estimates or phase labels. Odd cell counts are included; odd physical rings are not claimed.

The producer manifest is 318df810262ea9682f3f6fb9b388a001cd33919e2fde8f4ca7047169233b8f7d. The separate observable review is 8d26c955fb5500893be65dbbc6e639a86b230d299c9b59ed201a6f89728875ee. The earlier four coarse-bridge intervals remain independently accepted under 0a0b5864bb403c4d05419b375c93756791050e64b7dd100862358e2b5ab10e08. No old producer or reviewer seal was changed.

## 1. Inherited physical and analytic premises

The physical thermal inputs, all eighteen uniform seam/length cases, are inherited from their accepted independent reviews. The uniform n32 seed and its negative shifted physical64 anchor are checked against the accepted scalar and anchor provenance. The retained trial remains one vector of MPS bond dimension26; no physical spectral truncation or finite thermal-transfer rank is assumed.

The independently accepted observable review establishes Gibbs effect bounds κ32 ≤ 17/125 and κ64 ≤ 157/1000 at β0 = 49/4. These concern the actual uniform Gibbs state, not an identification of the MPS with the ground state. The local tensor reconstruction, complete L4/L6 physical checks, exact L32/L64 contractions and fidelity-to-effect proof remain separately sealed.

For the untwisted Gibbs state, translation reverses B and its spectral measure is symmetric. Together with ||B_L|| ≤ 3L/2, Golden–Thompson and the pointwise cosh second-moment bound give

    1 ≤ Z_eta,L(β0)/Z_0,L(β0) ≤ F_L,
    F_L = 1 + κL[cosh(β0·3Lr/2)−1].

The lower comparison holds at every positive inverse temperature. Therefore the spatial and thermal seed lower endpoints transport as S0/F32² and T0/F64². The reviewer verifies the two different physical lengths, their separate κ bounds, the squared denominators and the direction of every rounding.

Write c = (1+g)/2 = 1/(1+eta). The actual Hamiltonian is c(H0+eta B), the linear physical shift is c·700741/500000 per site, and actual inverse temperature is β/c ≤ β(1+r). The proof and code check this physical rescaling at every bootstrap window and in every finite bridge. No additional factor L is applied to the already-total H anchor.

## 2. All fourteen finite physical lengths

The missing cells2 through15 correspond exactly to even physical lengths4,6,…,30. For each length the checker loads the original rational purity C_L from the accepted uniform all-size review, at β0 = 49/4. It verifies the producer's ground-weight lower endpoint

    w_L ≤ (1 + sqrt(2C_L−1))/2.

Purity C_L > 1/2 implies a unique maximal Gibbs weight p0 ≥ w_L; p1 ≤ 1−p0. A directed strict inequality w_L > exp(β0 δ_L)(1−w_L) consequently certifies the positive rational finite uniform gap δ_L. The reviewer checks every saved δ_L and margin directly, without replaying the producer's milligap search or asserting that these lower bounds are optimal.

For each of the four radius/gap pairs (r,D), it then independently checks both equivalent sufficient routes:

    lower_L = [δ_L−3Lr]/(1+r) ≥ D,

and, directly from the accepted Gibbs weight,

    w_L > exp[β0((1+r)D+3Lr)](1−w_L).

The first follows by the eigenvalue perturbation bound 2||eta B_L|| ≤ 3Lr and multiplication by c ≥ 1/(1+r), with positive numerator. The second verifies the exact uniform gap required by the target, so no rounded logarithm enters the certification. All56 checks are strict beyond the claimed target. The weakest finite length is24, with perturbed finite lower bounds approximately .1036914, .0999067, .0974342 and .0959277 across the four rows, well above the respective targets.

Physical24 retains its accepted parity certificate with the physical48 MPS anchor. The audit explicitly checks this provenance label and inherits the underlying accepted physical purity. It does not invent a direct own-length24 anchor or recompute that physical evidence.

## 3. Complete bootstrap and late closure

The previously accepted positive-cell transfer represents the physical alternating partition function by powers of the positive trace-class operator A_g A_g*. The present intervals have g > 0 and inherit this analytic structural result with its pinned manifest. No product-of-two-self-adjoint-operators shortcut is used.

At cell seed n and actual inverse temperature τ, positive Schatten interpolation gives

    purity(M,τ) ≥ min(s sqrt(t),t) = C

for every integer n ≤ M ≤ 2n. The checker verifies C > 1/2 and the strict physical gap margin C−exp[β(1+r)D](1−C) > 0 in every saved window. Coordinates are checked as cell n, physical2n, β = 2^j·49/4, and every doubled window is present.

All saved 400-decimal-place sequential updates are checked exactly:

    s_new = G(s²t), t_new = G(t²s_new),
    G(x) = 1−(1−x)²/(2x²).

The new spatial endpoint is used in the thermal step. The four certificates have10,9,10,10 explicit windows,39 total. Their terminal cell sizes are8192,4096,8192,8192. In each row u = max(1−s,1−t) ≤ .01 and the exact directed terminal margin 1−5u exp[β(1+r)D] is strictly positive.

The independently rechecked constants imply u_next ≤ 5u², interpolation purity at least1−3u/2, and excited/ground ratio at most2u. Thus the terminal condition propagates to all further doubled windows. Together with the complete cells2..15 finite bridge and the cell16 initial window, every integer M ≥ 2 is covered without holes.

## 4. Arithmetic, mutations and preserved failures

The reviewer imports no producer implementation. It uses independent1600-bit dyadic enclosures,250 positive Taylor terms after reduction to an argument at most1/4, a geometric next-term tail, directed squaring/reciprocals and integer-square-root bracketing. These bounds are finer than the saved400-place decimal endpoints, including the very late nonzero defects. Producer decimal floors in the recurrence are checked exactly.

Only the four advertised certificates are numerically replayed. The32 producer search-candidate files remain pinned historical data; their15 rejections are not interpreted as no-go results or independently recertified here. Widths depend on a bounded search and are not asserted maximal.

Sixteen adversarial corruptions are rejected. They include omitted seed losses, swapped observable lengths, cell/physical confusion, omitted temperature rescaling, missing windows, inflated sequential updates, terminal scale errors, a missing physical24 bridge, omitted Weyl loss, omitted finite c scaling and a late purity falsely rounded to1.

The failed preliminary finite-bridge proposal is preserved in its own sealed producer package. Its floating candidate selection could be optimistic when a late defect rounded to zero; it produced no accepted interval certificate. The corrected producer used authorized exact rational bisection, retained rejected candidates and final per-gap checkpoints. This review validates only the final exact endpoint certificates. The older fixture-label and length32 wrapper failures also remain in their original audit histories and are not silently rewritten.

## 5. Resources and scope

The sole review run exited zero: independent wait4 2.586350 CPU seconds plus .157467666 launcher seconds, peak15728 KiB, wall2.745930396 seconds. It used hard8-second child and1-second parent CPU reservations,256 MiB, sole CPU5 affinity, verified post-exec limits and default/unblocked SIGXCPU, parent-death SIGKILL, an active CPU watchdog and external90-second whole-session watchdog. No guard fired, no descendants remained and no retry occurred.

The physical/local/observable checks and two interval audits together used18.081720854 observed child-plus-launcher CPU seconds before their three small sealing steps. Charging each sealing step its full2-second hard allowance yields a conservative cumulative review charge24.081720854 < 30 CPU seconds. All separate compilation attempts, including the explicitly corrected pre-exec failure, total16.872037073 < 30 CPU seconds. No new physical, thermal, H² or eigensolver job was launched for either interval audit.

This is an independently checked exact-arithmetic certificate plus analytic proof, not a formal proof-assistant derivation. Existing structural and physical premises remain inherited accepted evidence; this scalar extension does not physically rerun them. All source files, actual exact endpoint results, input pins and guard records are included in this separate review seal.
