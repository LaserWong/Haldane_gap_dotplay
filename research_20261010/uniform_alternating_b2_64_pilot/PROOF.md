# Physical64 staggered second moment and Gibbs upper bound

2026-10-11 04:06 UTC. Producer physical/scalar result, independent review required. No physical32 or H² production was performed; no new robust interval is claimed by this package.

## Result

For the unchanged periodic D26 MPS at64 physical spin-one sites, define B64=sum_odd h_j−sum_even h_j and b64=96. The exact contraction gives

    q64=<psi,B64² psi>/(96²<psi,psi>)
       = .007521781460785803... .

The defining exact rational is in scalar_result.json; its numerator and norm are the integers in pilot.out. The accepted N0_64 and TOTAL H0_64 agree exactly, before the new observable is accepted. Every one of the11 charge-block contributions is checkpointed and independently summed by the scalar checker.

Using only existing finite thermal bounds and energy-only fidelity, this yields the producer bound

    kappa64=Tr(rho_uniform,64 B64²)/96² <=157/1000=.157,

at beta0=49/4. The more precise outward scalar upper endpoint is approximately .1569041668671222. No energy variance/H² contraction is used. This kappa is a bound for the actual uniform Gibbs state, not an assertion that the D26 vector is the exact ground state.

## Physical contraction

The input b2_blocks.txt, hash1e63ba284062733ec459fd0f2125874b561b407ef7d722897f1923336ff58581, is the separately frozen local-insertion fixture output. It contains T,E_h,U=E_(h²),V=E_(h01h12+h12h01) in all11 charge blocks. Their physical formulas and direct full L4/L6 validation remain in uniform_alternating_b2_fixture.

The production source includes that frozen source's matrix/block-power helpers, with its main function renamed and NEVER executed. Its own main supports only length64 and only norm, first moment and B². It raises no resource limits from the inherited guards. The general binary helper has independent literal-block tests at all powers0..12 and both signs.

In each block, K=[[T,E_h],[0,−T]] is raised by exact binary composition to61. Let P61 andR61 be its upper diagonal and upper-right blocks. Because61 is odd, R61 is the required alternating disjoint insertion sum. Form P62=P61 T and T². Then

    N0_64 = sum_blocks Tr(P62 T²),
    H0_64 =64 sum_blocks Tr(P62 E_h),
    B2_64 =64 sum_blocks [Tr(P62 U)−Tr(P61 V)+Tr(R61 E_h)].

No dense3^64 physical object, no dense676×676 full transfer stack, and no doubled dense1352×1352 matrix is formed. The largest block side is162. No all-positive convolution is computed, so this is not an H² production run.

The norm/first-moment target file is the accepted independent uniform_smaller_second_initialization_review/anchors.out, hash217e4ba47ad3544f4f8ce384970cdc501c77a5916a7f5883a86cadeb42df1af2. Both mandatory integer identities pass. Global B2 is nonnegative and at most9216*N0, consistent with ||B64||<=96.

## Scalar energy and ground-weight checks

The n32 uniform seed supplies the accepted upper trace Q64 and thermal-purity lower C64 at beta0. All energies here use the consistent shift aL, a=700741/500000. Let

    mu=H0_64/N0_64+64a,
    E_lo=−71/10000,
    delta=19/100,
    w=(1+sqrt(2C64−1))/2.

The checker independently verifies with directed exponentials

    exp(−beta0 E_lo)>=Q64,
    w−exp(beta0 delta)(1−w)>0.

The first gives E0'>=E_lo. The second follows from physical Gibbs purity and proves the finite64 gap>=.19 and ground Gibbs weight>=w≈.9134631964156602. These are finite-volume inputs, not claims that the all-size gap is .19.

The accepted total trial mean is mu≈−.000009283946501609371. The spectral gap implies

    1−F <= epsilon=(mu−E_lo)/delta≈.03731955817630732,
    F=|<psi_normalized,ground>|²,
    f=1−epsilon≈.9626804418236927.

No residual norm is assumed. The exact mu matches the corresponding accepted shifted Rayleigh quotient.

## Sharper fidelity-to-effect inequality

Set O=B64²/96², so0<=O<=I, with trial expectation q=q64 and ground expectation alpha. For normalized trial and ground vectors, applying Cauchy–Schwarz separately to O^(1/2) and(I−O)^(1/2) gives

    sqrt(F)<=sqrt(q alpha)+sqrt((1−q)(1−alpha)).

If the certified f<=F satisfies f>q, solving this two-outcome angle constraint gives

    alpha <= [sqrt(f q)+sqrt((1−f)(1−q))]².                    (1)

Otherwise the safe bound is1. On the f>q branch the upper endpoint is nondecreasing in q and nonincreasing in f, so directed q-upper/f-lower substitution is valid. The present q is exact, f is a rigorous lower bound, and both square roots are rounded upward. Equation(1) gives alpha<=.0770336052496663... .

The uniform Gibbs state has ground weight p0>=w. Since all excited-state expectations of O are at most1,

    kappa64<=1−p0+p0 alpha<=1−w+w alpha<157/1000.

Every exact root, energy/gap margin, fidelity, alpha and kappa appears in scalar_result.json. The120-place directed checker reproduces them from original accepted seed/anchor inputs rather than treating a previously proposed fidelity number as an axiom.

## How the observable can enter a future trace certificate

For the untwisted uniform Gibbs state, one-site translation makes the spectral measurement of B symmetric. The pointwise inequality

    cosh(tx)−1 <= (x²/b²)[cosh(tb)−1],  |x|<=b,

and Golden–Thompson give

    1<=Z_eta,64(beta0)/Z_0,64(beta0)
      <=1+(157/1000)[cosh(96 beta0 eta)−1].

This is a substantially smaller thermal-seed denominator loss than the previous norm-only bound. It does not automatically give a wider all-size interval; that requires a new scalar bootstrap and its finite-size bridge. The physical32 companion is not present in this package and remains a separate authorization decision.

## Historical fixture mutation-label correction

The sealed fixture's bad[4] checks B2−L*adj even though the true B2 already contains−L*adj. That mutation doubles the adjacent subtraction; the historical prose called it omission incorrectly. Its physical formula, the direct equality and all result integers are unaffected. The frozen fixture remains unchanged.

The present scalar checker verifies a correctly named omission using the saved64 checkpoints:

    altered_B2=B2+64*sum_blocks(adjacent_symmetric).

This removes the adjacent subtraction and differs exactly from the correct B2. The rejected integer is recorded. No additional physical contraction or numerical retry was needed for this correction.

## Resources, checkpoints and reproducibility

The sole physical pilot used independent wait4 user16.783404CPU seconds plus system.402411=17.185815CPU seconds; peak35636KiB; wall17.759526232seconds; exit0. The child hard CPU cap was59seconds and parent cap1second, giving the authorized aggregate60 ceiling. CPU4,256MiB address space, default/unblocked SIGXCPU and parent-death SIGKILL were verified after exec. An external180-second wall watchdog remained armed and did not fire. Every block was written to a unique checkpoint before proceeding. No unexpected retry occurred.

Compilation was separate:6.886386CPU seconds,203976KiB, below its30CPU-second/512MiB cap. This does not consume the physical pilot's60-second budget. The cheap scalar analysis uses a3CPU-second/256MiB cap and runs in milliseconds. It forms no physical matrices.

Reproduce in a disposable directory preserving the frozen helper and input paths, because the guarded runner refuses an existing attempt and result/checkpoint paths are never overwritten. Reproduction of the physical run requires its own authorization. Existing fixture, interval, structural and root files were not modified. This is a producer exact-integer contraction and scalar proof, awaiting independent review.
