# Wider intervals from exact H²32/64 variance

2026-10-11 04:55 UTC. Producer exact interval proof; independent observable/scalar and interval composition review required. No physical contraction occurs in this package. Previously accepted intervals and source seals remain unchanged.

## 1. Claim and parameters

At physical even length L=2M, integer M>=2, use periodic spin-one unit exchange h_j=S_j dot S_(j+1), and

    H_M(g)=sum_j[h_(2j−1)+g h_(2j)],
    H0=sum_j h_j, B=sum_odd h_j−sum_even h_j,
    c=(1+g)/2, eta=(1−g)/(1+g), H_M(g)=c(H0+eta B).

The designated exchange stays one. For each exact radius r in README.md, all |eta|<=r, equivalently g in[(1−r)/(1+r),(1+r)/(1−r)], have a unique finite-volume ground state and a physical-unit gap at least the associated D. The four pairs are

    (751/5000000,1/50), (2089/10000000,3/200),
    (99/400000,1/100), (109/400000,1/200).

Only even physical rings are claimed. The accepted original gap and earlier robustness results are not relabeled or overwritten. These new radii are sufficient, not optimal.

## 2. New finite Gibbs effect inputs from energy variance

The unchanged D26 trial has separately produced exact total variances

    sigma32²=.0002629779063020885...,
    sigma64²=.0004964120744254386... .

They are defined by the exact integer fractions(H2*N−H²)/N² in the physical producer packages, not by these displays. Those packages require exact N/H and all11 same/adjacent block identities against accepted anchors/checkpoints before accepting H². Their manifests are

    uniform_alternating_h2_32_companion:
      5e6bb98a58c8b4f72a3199061bf23488749e11b80fe7177080c86760c0839dd0,
    uniform_alternating_h2_64_pilot:
      a6552c8c5de014a0ffc603e98e96b5e65752892a3752fab6a107d97722898e50.

The already accepted B² expectations q32=.01507219528810355... and q64=.007521781460785803... are unchanged.

At beta0=49/4, original trace upper Q and exact shifted trial mean mu give actual ground Gibbs weight w>=exp(−beta0 mu)/Q. Finite energy/gap endpoints are separately checked by exp(−beta0 E_lo)>Q and w−exp(beta0 delta)(1−w)>0. Energy-only fidelity F>=1−(mu−E_lo)/delta>1/2 selects the ground-overlap branch.

For the exact trial variance, the spectral pairwise identity gives

    sigma²>=F(1−F)delta²,
    1−F<=[1−sqrt(1−4sigma²/delta²)]/2

when the discriminant is nonnegative, retaining the minimum with the energy-only bound. This improves infidelity to at most.0053224825874 and.0129844639541 at32/64.

For0<=O=B²/(3L/2)²<=I, the sharp fidelity-to-effect inequality yields

    alpha_ground<=[sqrt(fq)+sqrt((1−f)(1−q))]²,
    kappa_L=Tr(rho0 O)<=1−w+w alpha_ground.

The producer-directed bounds are

    kappa32<=969/10000=.0969,
    kappa64<=119/1000=.119.                              (1)

Their full scalar proofs and independent review are separate from this interval composition. This package pins the exact producer inputs and does not silently treat their historical pending status as review acceptance. Any final independent interval review must verify acceptance of both observable packages.

## 3. Finite seed transport and temperature

For even L, centering each h_j by1/2 gives ||B_L||<=3L/2. One-site translation fixes the actual untwisted uniform Gibbs state and reverses B. Therefore its spectral B distribution is symmetric and its B mean is zero. Gibbs variational convexity gives Z_eta>=Z0. Golden–Thompson gives the upper comparison by Tr(rho0 exp(−beta0 eta B)), not the reverse direction.

The pointwise spectral chord

    cosh(tx)−1<=(x²/b²)[cosh(tb)−1], |x|<=b,

and(1) imply, for |eta|<=r,

    1<=Z_eta,L/Z0,L<=A_L(r),
    A_L(r)=1+kappa_L[cosh(beta0*(3L/2)*r)−1].           (2)

This is only an untwisted finite-trace comparison. The original I/P physical inputs are used inside the accepted uniform seed; no translation-zero statement is asserted for a twisted trace.

The accepted uniform physical32 seed, with own physical64 D26 trial anchor, supplies S0,T0. Its18 original beta49/4 thermal inputs at physical lengths4..12, signed-transfer moment bounds and per-site shift a=700741/500000 remain unchanged. The periodic trial is one-site translation invariant, so its B expectation is exactly zero.

Choose actual inverse temperature tau0=beta0/c and shifted per-site energy ca. The trial Boltzmann numerator is unchanged because its perturbed shifted mean is c times the uniform shifted mean. Consequently at cell base16,

    s>=S0/A32(r)², t>=T0/A64(r)².                      (3)

No perturbative extensive norm is used at unbounded length. All losses in(2)–(3) are confined to finite seeds; subsequent recursion uses the actual alternating model.

## 4. Positive transfer, integer windows and the infinite tail

The independently accepted cell-history construction represents the transfer as A_g A_g* between the proper positive-history measure spaces. It is positive trace class for g>=0, with the physical trace identity for every integer M>=2. All g in these intervals are positive. No unjustified product of self-adjoint operators is assumed positive.

Positive l^p monotonicity for the numerator and Holder interpolation for the denominator give, at every integer cell base n and n<=M<=2n,

    T(M,tau)>=s^(2−M/n)t^(M/(2n))>=C=min(s sqrt(t),t).

Since actual tau=beta/c<=beta(1+r), the directed condition

    C−exp[beta(1+r)D](1−C)>0

proves uniqueness and gap at least D throughout the entire integer window. The sequential updates are

    G(x)=1−(1−x)²/(2x²),
    s_new=G(s²t), t_new=G(t² s_new),
    (n,beta)->(2n,2beta).

Every legal-domain input/output is checked. At u=max(1−s,1−t)<=.01, the next common defect is at most5u². The directed terminal test5u exp[beta(1+r)D]<1 therefore closes every later integer-cell window by the previously accepted small-defect proof.

The four final rows have10,9,9,9 finite windows, closing at cell8192,4096,4096,4096. Their terminal defects are approximately4.78509e−56,5.86673e−22,3.25480e−15,2.73602e−8; terminal margins are approximately.267273,.204123,.317128,.113491. Exact rational margins, not these displays, are saved in certificate.json. All37 finite windows and all four tails pass strictly.

## 5. Same accepted length-specific finite bridge

The accepted uniform_gap_0248_all_sizes_review exact purities at beta49/4 for physical4,6,...,30 are retained. For each C_L>1/2, w_L=(1+sqrt(2C_L−1))/2 gives a finite gap lower delta_L via

    w_L−exp(beta0 delta_L)(1−w_L)>0.

The unchanged rational gap list in physical order4,6,...,30 is

    .907,.511,.427,.408,.388,.294,.245,.221,.210,.207,
    .113,.210,.214,.217.

These are exact multiples of1/1000, rechecked by directed inequalities. The physical24 purity explicitly retains its parity/MPS48 provenance; no own24 trial is invented. Analytic physical2/3 are outside this alternating M>=2 scope.

At each of these14 finite lengths, Weyl gives

    gap(H_M(g))>=(delta_L−3Lr)/(1+r).

The checker verifies this lower bound is at least D and also checks the required normalized gap directly against w_L. All56 finite comparisons pass. Physical24 remains the smallest finite lower bound; its four values are about.1021702540,.0979387406,.0951564488,.0933545609, all well above the requested gaps. Combined with the overlapping cell16-and-larger bootstrap windows, every integer M>=2 is covered.

## 6. Exact search and resource gate

The search is entirely rational and begins by rechecking the four previously accepted radii from uniform_alternating_second_moment_finite_bridge_retry1. It then checks upper radius1/2500 and performs bounded exact bisection. Every candidate is written to an exclusive numbered checkpoint, including its rejected sufficient-test reason and endpoints. No floating tail test or zero-defect shortcut appears.

Six bisection cycles completed. The final radii are rounded down to a1e−7 grid and exactly rechecked. There are36 candidate records,19 rejected tests, four final gap checkpoints and no unexpected retry. Search upper brackets are unresolved sufficient-test proposals, not no-go claims or optimality results. The search stopping time can affect how many optional cycles finish; the frozen final rational certificates are independently replayable without repeating the search.

Arithmetic uses400 decimal places, exact squared root brackets,220 positive Taylor terms after reducing exponential arguments below1/16, a geometric next-term remainder, and outward repeated squaring. Cosh and gap exponentials round upward; seed, root and window lower endpoints round downward. The final smallest defect is around1e−56, far above the directed grid floor.

This was a newly authorized separate30CPU-second/256MiB scalar gate, not a reset of earlier budgets. Child hard limit28CPU seconds and parent reserve1 keep the hard aggregate below30. The independent launcher enforces sole CPU4, an active CPU kill threshold27seconds and90-second external wall guard; postexec checks verify hard limits, default/unblocked SIGXCPU and parent-death SIGKILL.

Observed child24.454525CPU seconds; parent.501166278CPU seconds; total24.955691278, peak16312KiB, wall25.153019845seconds,1196 active polls; exit0, no watchdog or retry. Charging the full parent reserve instead gives25.454525CPU seconds, still below30. No physical contraction, compiler, eigensolver or thermal campaign ran in this gate.

All previous physical, scalar, review and failure-ledger seals are pinned and preserved. Root documents and remote state are unchanged. New interval promotion requires the independent H² and final interval reviews; earlier accepted results remain authoritative meanwhile.
