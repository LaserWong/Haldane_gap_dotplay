# Independent variance-refined robustness review

2026-10-11 04:57 UTC / 2026-10-11 00:57 America/New_York (EDT).

## Accepted closed intervals

For every integer cell count M ≥ 2, consider the periodic spin-one alternating chain

    H_M(g) = Σ_(j=1)^M [S_(2j−1)·S_(2j) + g S_(2j)·S_(2j+1)],
    S_(2M+1) = S_1.

The designated first bond has coefficient one. Physical length is L = 2M and full Hilbert dimension is3^(2M). The ground state is unique and the physical-unit gap obeys:

- gap ≥ .020 on [4999249/5000751,5000751/4999249];
- gap ≥ .015 on [9997911/10002089,10002089/9997911];
- gap ≥ .010 on [399901/400099,400099/399901];
- gap ≥ .005 on [399891/400109,400109/399891].

These are exact closed intervals, equivalently eta = (1−g)/(1+g) with radii751/5000000,2089/10000000,99/400000 and109/400000. Odd cell counts are included; odd physical rings are not claimed. These are sufficient neighborhoods rather than optimal phase boundaries or actual-gap estimates. They do not connect the near-uniform neighborhood to the separate weak-dimer regime.

The final producer manifest is3c6bfbaedd753160c7b22bf3fd0839ce64330735e1c4ec8437d5e37ae0129d56. The new independent H²/variance review is cca4335ac42dd34b2e75528a89a2834998d9126c5abcb73df965a344da669f60. The preceding finite-purity interval review4700be5942eac716532d52c82aef89e8508334e61da511b26f2dd75a7a2272c3 and every earlier seal remain unchanged. The producer's historical pending-H² flag is resolved by the new independent acceptance; its frozen file is not rewritten.

## 1. Independently accepted physical premises

The uniform physical thermal data, n32 seed, physical64 negative shifted anchor, complete D26 local transfer insertions and periodic B²/H² conventions are inherited from their independent accepted evidence. The new H² review independently reconstructs all22 physical32/64 sector checkpoints, exact variances and scalar premises. It proves

    κ32 = Tr(ρ0,32 B32²)/48² ≤ 969/10000,
    κ64 = Tr(ρ0,64 B64²)/96² ≤ 119/1000,

at β0 = 49/4. Those are actual Gibbs-state effect bounds. The proof separately checks Rayleigh-derived Gibbs ground weights, finite energy lower bounds, finite gaps and the correct F > 1/2 branch of the pairwise variance inequality. Neither a trial expectation nor a small residual is substituted for a Gibbs bound.

This interval audit verifies the complete H² review manifest and reads its independent scalar endpoints. It imports no producer implementation and does not repeat a physical contraction. There remains one retained D26 trial vector, not an enlarged linear trial space or a finite thermal-transfer rank hypothesis.

## 2. Seed transport and physical normalization

With B_L the alternating bond sum, ||B_L|| ≤ 3L/2 follows by centering each spin-one bond at−1/2; the scalar parts cancel. Uniform translation reverses B while fixing the untwisted Gibbs state. The Gibbs variational lower bound, Golden–Thompson upper bound and pointwise second-moment cosh inequality imply

    1 ≤ Z_eta,L(β0)/Z_0,L(β0) ≤ F_L,
    F_L = 1 + κL[cosh(β0·3Lr/2)−1].

The lower comparison holds also at2β0, so the actual perturbed seed satisfies

    S ≥ S0/F32²,       T ≥ T0/F64².

The checker independently bounds the two cosh factors and verifies both length-specific κ values, both denominator squares and every rounding direction. It also matches S0, T0 and the shifted total Rayleigh quotient with the accepted n32/physical64 evidence. The H numerator is already total energy and is not multiplied by64 again.

Write c = (1+g)/2 = 1/(1+eta). Then H_M(g) = c(H0+eta B), the physical shift is c·700741/500000 per site, and physical inverse temperature is τ = β/c ≤ β(1+r). The actual designated exchange remains one at both interval endpoints, including g > 1. The checker verifies this rescaling in every window and bridge.

## 3. All finite missing cell sizes

Cells2 through15 are exactly physical lengths4,6,…,30. At each length the original accepted rational purity C_L at β0 = 49/4 is loaded from the uniform all-size review. The checker independently brackets w_L = (1+sqrt(2C_L−1))/2 from below and verifies the saved rational positive finite gapδ_L through

    w_L > exp(β0δ_L)(1−w_L).

For each of the four radius/target pairs(r,D), all fourteen rows must satisfy both

    [δ_L−3Lr]/(1+r) ≥ D,

and the direct target check

    w_L > exp[β0((1+r)D+3Lr)](1−w_L).

The first is the finite-volume Weyl bound, using2||eta B_L|| ≤ 3Lr and positive numerator before c scaling. The second independently checks the exact uniform gap required for the target. Thus no rounded logarithm is accepted as a certificate. All56 bridge checks pass with strict slack.

Physical24 is the weakest finite row in all four cases. Its perturbed gap lower bounds are approximately .1021703,.0979387,.0951564 and .0933546, respectively. Its source remains the accepted parity certificate with the physical48 MPS anchor, explicitly checked by the reviewer. No direct own-length24 anchor is invented.

## 4. Complete integer-cell bootstrap and asymptotic tails

The previously accepted positive-cell construction represents the actual alternating partition function as Tr[(A_g A_g*)^M], with A_g Hilbert–Schmidt between the appropriate bond-history spaces. All present g are positive. This analytic structural premise is inherited with its verified manifest; no unjustified product of self-adjoint operators is substituted.

Positive Schatten interpolation gives, for every integer n ≤ M ≤ 2n,

    purity(M,τ) ≥ min(s sqrt(t),t) = C.

The reviewer checks C > 1/2 and C > exp[β(1+r)D](1−C), proving uniqueness and the desired physical gap across every complete window, including odd M. It verifies each cell/physical coordinate, doubled inverse temperature, window endpoint and strict rational margin.

Every400-place directed sequential update is checked exactly:

    s_new = G(s²t), t_new = G(t²s_new),
    G(x) = 1−(1−x)²/(2x²).

The new spatial endpoint is used in the thermal update. The four certificates contain10,9,9,9 finite bootstrap windows,37 total. Terminal cell bases are8192,4096,4096,4096. At each terminal state, u = max(1−s,1−t) ≤ .01 and5u exp[β(1+r)D] < 1.

The independently checked constants imply u_next ≤ 5u² and excited/ground Gibbs ratio at most2u. Hence the terminal inequality propagates to all future doubled windows. The finite bridge covers cells2..15, the bootstrap starts at16, and the doubled windows overlap without holes. Their union covers every integer M ≥ 2.

## 5. Arithmetic, scope and robustness tests

Independent enclosures use1600-bit dyadics,250 positive Taylor terms after argument reduction to at most1/4, a geometric remainder, directed squaring/reciprocals and exact integer-square-root brackets. They are finer than the producer's400-decimal-place endpoints. The stored decimal floors are separately checked as exact rationals, including the very late nonzero defects.

Only the four advertised final endpoint certificates are numerically replayed. Search candidates are preserved and hashed as provenance but are not used to infer optimality or no-go statements. No floating search result is accepted as proof.

Sixteen corruptions are rejected, including omitted seed losses, swapped observable-length labels, wrong coupling endpoints, cell/physical confusion, omitted temperature scaling, missing windows, inflated sequential updates, terminal-coordinate errors, a missing physical24 bridge, omitted Weyl loss, omitted finite c scaling and a late purity rounded falsely to1.

The original producer failures and prior review ledgers remain immutable. This exact-arithmetic and analytic review is not a formal proof-assistant derivation. It reuses accepted physical/structural premises rather than physically repeating them.

## 6. New-gate resource accounting

This interval audit used one run: independent wait4 3.709270 CPU seconds plus .257206511 launcher seconds; peak16028 KiB; wall3.922886626 seconds. Hard reservations were8 child CPU seconds plus1 parent second,256 MiB, sole CPU5, verified post-exec limits/signals/affinity, parent-death SIGKILL, active aggregate CPU polling and an external90-second whole-session watchdog. Exit was zero, no watchdog fired, no descendants remained and no retry occurred.

The completed H² physical/scalar review charged15.172304705 observed CPU seconds. This interval review adds3.966476511, giving19.138781216 observed scientific CPU seconds. Each of the two completed sealing steps is conservatively charged its full one-second reservation, so the new gate's final charge is21.138781216 < 30 CPU seconds. Completed runs release unused reservations only after their measured terminal outcomes; failed reservations would be retained, but no review attempt failed in this gate. The separate compiler charge remains4.511079611 < 30 CPU seconds. Older gates are not reset or mixed into this ledger.

All exact output, source, input pins, guard records, independent mathematical argument and final acceptance seal are preserved separately from the H² observable seal and all prior interval seals.
