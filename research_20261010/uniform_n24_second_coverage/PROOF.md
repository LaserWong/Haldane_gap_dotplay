# Individual24/25 coverage probe

2026-10-10 22:32 EDT / 2026-10-11 02:32 UTC. Exact partial producer result and bounded diagnostic; independent review pending.

## Result and stopping point

At beta49/4, the exact parity-dependent canonical interpolation certifies unique ground state and gap>=.0023 for the isolated even lengthL24, with purity lower bound.6813771416499027. For oddL25 the same exact construction supplies only.37345909940502603, below1/2, so it certifies no positive gap or uniqueness there. This is a failure of this sufficient bound, not a statement about physical purity or the actual gap.

Consequently no contiguous coverage extension below26 is claimed. The separate accepted/pending26-and-up result is unchanged, initialization remains30, and L24 is an additional isolated finite size. No n24 startup, no n22 computation, and no minimum-size or all-method obstruction is asserted.

## Exact construction and own anchor

Use uniform periodic spin-one Heisenberg with coupling1 and shift700741/500000. All18 beta49/4 thermal inputs, signed J/N moment intervals4..12 and supports are inherited from their independent audits. The frozen smaller-initialization package provides the exact N24 polynomial majorant. For length48 the safe upper trace here is the twelfth-moment packing envelope; a stronger polynomial is not silently substituted.

The new physical contraction has its own N0_48=Tr(T^48)>0 and H0_48=48Tr(T^46 O). Its total shifted Rayleigh is exactly negative. check_anchor.py additionally matches both integers against the already accepted independent48 output, with source hash saved. The trial is one D26 MPS in a3^48-dimensional physical Hilbert space. It is not an ED computation or reuse of a72-site quotient.

certify.py reconstructs the positive dominant J atom via the strict packing contradiction from Z48(beta)>1 and the accepted negative-J support cap. It bounds residual mass and produces S(24,beta0),T(48,beta0). Its failed uniform-window constant is saved only as a diagnostic. certify_missing_lengths.py applies the length-resolved formula from uniform_n26_second_coverage/PROOF.md:

    p=L/24, K=S^2T>1/2,
    w=(1+sqrt(2K-1))/2, rho=(1-w)/w, D=T/(1+rho^2),
    C_L=S^(2-p)D^(p/2)                         if L even,
    C_L=S^(2-p)D^(p/2)(1-rho^p)               if L odd.

For even powers the doubled-temperature numerator's subleading spectrum contributes nonnegative terms; for odd powers its absolute tail must be subtracted. Dominant positivity follows from the valid all-integer physical trace identity, not positivity of every eigenvalue. Holder denominator interpolation uses even endpoints24,48. Directed rational powers/roots and Taylor exponentials are checked exactly. At24 the positive exponential margin proves .0023; at25 the saved negative margin and C<1/2 are only a proof-method miss.

## Bounded cooling follow-up

A permitted floating proposal scan uses ell in{12,16,18,20,22,24} and rational grid r=1.00..3.00 in steps.01. For each it cools the identity and equivalent pi-seam physical traces using the valid Gibbs norm inequality. It uses total D=(Jell+3Nell)^r, nonidentity upper E=Jell^r, cooled trivial upper tau=(D+3E)/4, and the two-sector convex tail endpoints described in the frozen n28 package. The physical48 anchor supplies the corresponding Boltzmann forcing at beta=r*49/4; thermal ground-plus-tail cooling supplies T48 at that same beta. No distinct-temperature physical trace is fabricated.

511 candidates satisfy its preliminary forcing geometry. None passes the individual odd25 gate. The best sampled generic cooled bound is approximately.2496303211 at ell20,r1,beta49/4, weaker than the directly retained signed-moment bound. The coarse sector relaxation loses information even at r1. This is only a finite floating search of this parameterized sufficient method, not an exact interval exclusion over temperature, an optimality proof, or a reason to claim a new thermal campaign is necessary. Its proposals would require exact scalar replay if positive; none were accepted.

## Resources, replay and status

Fresh48 contraction:10.5412CPU seconds,32232KiB, CPU5, hard100MiB/60CPU-second process limit. All producer fresh anchors68,64,60,56,52,48 together:52.63721CPU seconds, below the original60 budget. The reviewer already has a fresh independent48 rebuild/contraction. The exact prefix and cooling scripts run CPU2 with hard30CPU-second/256MiB limits; length-resolved proof.429CPU seconds. An early scalar call before the anchor finished returned missingN0_48 without accepted output, then was rerun only after completion.

Replay in a disposable copy: python check_anchor.py; python certify.py; python certify_missing_lengths.py; optionally python cooling_pilot.py. No thermal campaign, largerD, tensor optimization, remote edit or alteration of previously sealed evidence. This package is a stopping-point diagnostic plus isolated even24 certificate, not a new contiguous all-size theorem.
