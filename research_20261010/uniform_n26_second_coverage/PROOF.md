# Coverage26 by resolving the two missing integer lengths

2026-10-10 22:29 EDT / 2026-10-11 02:29 UTC. Exact producer certificate; independent review pending.

## Positive result and scope

Uniform periodic spin-one Heisenberg chain, unit bilinear coupling, beta0=49/4 and shift700741/500000. A fresh exact MPS52 anchor plus the independently validated18 thermal inputs certify unique ground state and gap>=23/10000=.0023 at the two individual lengths26 and27. With the independently reviewed coverageL>=28 at.0179, this yields gap>=.0023 and unique ground state at every integerL>=26.

Bootstrap initialization remains30. This is a coverage extension only. Existing stronger bounds from28,30,32,34 remain intact. Neither n26 initialization nor a minimum seed is proved. No n24 computation is included.

## Why the first attempted window failed

certify.py preserves the initial canonical26/52 seed construction and failed full-window constant. Using the same signed moment method as the smaller-initialization package, it obtains

- S(26,beta0)>=.848048256921175;
- T(52,beta0)>=.8662555116602277;
- positive dominant J eigenvalue greater than ell=.9999543523.

All are exact rational lower bounds in certificate.json, with decimals here for orientation only. The fresh physical anchor is R52≈-3.1335486307754155e-5, with positive exact norm. The full-window simplified bound is C≈.495981255822436<1/2, so that particular constant certifies no positive gap uniformly over26..52. This failure is retained. It does not rule out shorter subwindows or individual integer lengths, nor does it upper-bound actual physical purity.

Only26 and27 remain uncovered once the n28 result is available. No uniform constant for unnecessary larger lengths is required.

## Exact length-dependent signed interpolation

Use the canonical exchange identity and the already reviewed transfer argument in root_review/FINITE_WINDOW_INTERPOLATION.md. Put

    K=S^2 T>1/2,
    w=(1+sqrt(2K-1))/2,
    rho=(1-w)/w<1,
    D=T/(1+rho^2).

The self-adjoint doubled-temperature transfer has a unique positive dominant eigenvalue: its even-base purity exceeds1/2, and a negative dominant eigenvalue would contradict physical trace positivity at all sufficiently large odd lengths. Relative absolute n-th tail mass is at most rho. For p=L/n>=1, convexity bounds relative L-th tail by rho^p. The even numerator tail is nonnegative and may be discarded. For odd L it must instead be subtracted.

Combined with absolute-spectrum Holder interpolation of the denominator between the even endpoints n and2n, the same canonical derivation gives, for n<=L<=2n:

    T(L,beta) >= S^(2-p) D^(p/2),                    L even;
    T(L,beta) >= S^(2-p) D^(p/2) [1-rho^p],          L odd.

This retains the actual p and parity rather than replacing1-rho^p by1-rho and minimizing the remaining factor over the whole interval. No monotonicity of purity in physical length or relabeling of canonical/thermal endpoints is assumed. The transfer identity's original valid rangeL>=4 covers all lengths here.

certify_missing_lengths.py takes p=1 at26 and27/26 at27. Positive powers of S,D are rounded downward; rho^p is rounded upward before subtraction. Integer-root bisection encloses all rational powers with explicit power checks. For both exact lower purities it checks C-exp(beta*.0023)(1-C)>0. Results:

- L26: C>=.747990627911218, margin>.48877;
- L27: C>=.5070738839110758, margin>.000062074.

A Gibbs purity>1/2 gives a unique ground state, and the checked exponential inequality gives the gap bound. The finite set{26,27} plus[28,infinity) has no missing integer. The n28 dependency is pinned to manifest66c710bfc302c3f6a220a3162d933add710bfe51aef6fbcf1e256d6725430b55. The underlying startup30 dependency is fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84.

## Physical provenance and resources

The unchanged physical D26 blocks are audit/mps/mps_blocks.txt. The frozen sibling contract_ground executable performs N0_52=Tr(T^52),H0_52=52Tr(T^50 O), not a per-bond energy. Physical Hilbert dimension is3^52, bond dimension26, one trial state. Positive norm and negative total shifted Rayleigh are checked exactly. The new52 contraction used7.35464CPU seconds/32156KiB, CPU5, hard100MiB/60CPU-second process cap. Cumulative producer contractions60/64/68/56/52 used42.09601CPU seconds, below the original60 budget. Independent52 tensors/contraction have been prepared by the reviewer; scalar/parity acceptance is separate.

The first scalar launcher unnecessarily repeated a gap grid even after a zero-gap full-window failure; it was interrupted viaSIGINT (exit130) at02:28:02UTC. It never produced an accepted certificate. Its hard120CPU-second/256MiB limit and CPU2 affinity were active, but no terminalCPU measurement was saved. The launcher began02:26:20UTC including the7.35-second anchor; its wall interval bounds this interrupted phase, rather than a fabricated preciseCPU charge. The corrected final full-window replay runs once and uses2.6325CPU seconds. A separate authorized30CPU-second/256MiB length-resolved run uses.252CPU seconds/~11MiB. All scalar work is singleCPU2. No new thermal campaign, ED, tensor optimization or remote changes.

Reproduce with python certify.py, then python certify_missing_lengths.py. The first preserves the failed uniform attempt; the second is the positive result. INPUT_SHA256.json and LENGTH_INPUT_SHA256.json pin sources. Run only in a disposable copy if preserving the sealed outputs. No previous sealed package or root documentation was changed.
