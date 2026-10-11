# Exact physical32 H² and variance-refined fidelity

2026-10-11 04:51 UTC. Producer result requiring independent review. No new alternating-chain interval or new thermal trace is computed.

## 1. Structured wrapper and unchanged physical kernel

This is the separately authorized32 companion to uniform_alternating_h2_64_pilot, manifest a6552c8c5de014a0ffc603e98e96b5e65752892a3752fab6a107d97722898e50. That64 source and every prior seal remain unchanged. WRAPPER_DIFF.txt lists every source change: structured LENGTH32, CHILD_CPU_CAP19 and corresponding guard/result labels. CONVOLUTION_POWER=LENGTH−3 is29 and CONVOLUTION_SIGN remains+1. No unrestricted numeric replacement or altered side162 is used.

The same frozen fixture.cpp helper and b2_blocks.txt are reused, hashes afaf61d76e1de0dceae377b0c61923bf3d2facf11f85a3915888a19707ad5214 and1e63ba284062733ec459fd0f2125874b561b407ef7d722897f1923336ff58581. Independent observable review8d26c955fb5500893be65dbbc6e639a86b230d299c9b59ed201a6f89728875ee already validates the local operators and complete physical L4/L6 H² identities, including closing bonds, and the binary block helper for both signs.

At L32 let Kplus=[[T,O],[0,T]], P29=(Kplus^29)_upper-diagonal, R29=(Kplus^29)_upper-right and P30=P29*T. Each block contributes

    N=Tr(P30*T²), H=32Tr(P30*O),
    H2=32[Tr(P30*U)+Tr(P29*V)+Tr(R29*O)],

where O=E_h,U=E_(h²),V=E_(h01h12+h12h01). All11 blocks retain sides1,8,32,80,136,162,136,80,32,8,1. Each norm, total H, same-bond and adjacent scalar exactly matches the frozen physical32 B² checkpoint before H² is accepted. The final N/H match the independent uniform_gap_0248_all_sizes_review/anchors.out, hash70562d55010e46b5fea6aeb10609d846145c263dffe88fc8236cd5f4b8c088b5. The scalar checker resums all checkpoints and repeats all four-field identities.

There is one periodic D26 trial vector, not a larger linear variational space. Full Hilbert dimension3^32 is never constructed. H² is nonnegative, at most(2L)²N, and the exact variance numerator H2*N−H² is nonnegative.

## 2. Variance and actual finite thermal premises

The total variance, invariant under a scalar energy shift, is

    sigma²=(H2*N−H²)/N²=.0002629779063020885... .

The exact defining fraction is saved in scalar_result.json. It is neither a per-site variance nor a square root. H/N is already the total energy.

Read the original accepted physical32 own-length certificate from uniform_gap_0248_all_sizes/certificate.json at beta0=49/4, using its exact trace upper Q32, purity C32 and total shifted Rayleigh quotient mu=H/N+32a, a=700741/500000. The code verifies mu exactly against that certificate. For q=<B32²>/48², use the independently accepted physical32 B² result, q≈.01507219528810355.

Variationally E0'<=mu, so the actual ground Gibbs weight obeys w>=lower_exp(−beta0 mu)/Q32≈.9387875477507066. The directed checks

    lower_exp(−beta0 E_lo)>Q32,
    w−upper_exp(beta0 delta)(1−w)>0,

pass at E_lo=−627681/100000000 and delta=1783/8000=.222875. They give E0'>=E_lo and finite32 uniqueness/gap>=delta. This is not an all-size.222875 claim.

The energy-only infidelity is epsilon0=(mu−E_lo)/delta≈.02313597799061205<1/2. This already identifies the correct ground-overlap branch.

## 3. Pairwise variance fidelity and Gibbs effect

Writing F for trial ground overlap, the spectral pairwise variance satisfies

    sigma²=sum_(i<j)p_i p_j(E_i−E_j)²>=F(1−F)delta².

Since the energy-only premise gives F>1/2, inversion on that branch yields

    epsilon=1−F<=[1−sqrt(1−4sigma²/delta²)]/2.

The checker takes the minimum with epsilon0 and rounds the variance endpoint upward. Here

    epsilon<=.005322482587375599...,
    F>=.9946775174126244... .

The strict improvement threshold delta² epsilon0(1−epsilon0) is approximately.0011226507985878738, comfortably above the observed variance. No residual/variance estimate is assumed: its exact fraction comes from the new H² contraction.

For the effect O=B32²/48²,0<=O<=I, Cauchy applied to sqrt(O) and sqrt(I−O) gives the previously derived sharp fidelity-to-effect endpoint

    alpha_ground<=[sqrt(fq)+sqrt((1−f)(1−q))]²,
    f=1−epsilon>q.

Bounding excited effect expectations by1 and using actual Gibbs ground weight>=w gives

    kappa32=Tr(rho0 B32²)/48²<=1−w+w alpha_ground
       <=.09685318612605492...<969/10000=.0969.

Every root, finite energy/gap margin, fidelity, ground effect and kappa endpoint is recorded exactly. This is a producer upper bound for the untwisted uniform Gibbs state at beta49/4. Its use in wider alternating intervals awaits independent observable/scalar review and a separate directed bootstrap.

## 4. Directed arithmetic and no scalar retry

The already corrected64 scalar method is used from the outset. Exponential arguments are enclosed by adjacent dyadics with denominator2^128 before Taylor expansion; monotonicity transfers the enclosure to exp. The exact potentially large variance fraction is never approximated. Exponentials use140 positive terms after reduction below1/16, a geometric tail bound, reciprocal endpoints for negative arguments and outward squaring. Root brackets are verified by exact integer squaring. Final endpoints use a120-place grid; this does not overstate the accuracy of the explicitly bracketed input argument.

The independently guarded scalar run completed on its first attempt: wait4 .493570CPU seconds, parent.011676827CPU seconds, peak10496KiB,25 active polls, wall.526423781seconds. Child cap2CPU seconds and parent reserve1,256MiB CPU4,15-second wall guard. No failed scalar or numerical retry occurs in this companion.

## 5. Production/compilation accounting

The physical job was separately authorized for20 aggregate CPU seconds,19 child+1 parent,256MiB CPU4 and90-second wall timeout. After exec it verifies hard CPU/address-space caps, sole affinity, default/unblocked SIGXCPU and parent-death SIGKILL. An independent guard actively polls and kills above18CPU seconds, enforces the wall timeout, reaps with wait4 and saves all checkpoint files exclusively.

Physical job:7.587519 user+.048596 system=7.636115CPU seconds, parent.109374172CPU seconds, peak25440KiB, wall7.797718358seconds,189 active polls, exit0, no watchdog or retry.

Physical plus scalar total is

    7.636115+.109374172+.493570+.011676827
      =8.250735999CPU seconds of20.

Replacing both measured numerical parent costs by full one-second reserves gives10.129685CPU seconds, still below20.

The64 executable was intentionally fixed-length, so a new structured32 wrapper was compiled under the remaining original separate30CPU compilation allowance. Its child cap20 and parent reserve1 fit the remaining22.870108335 allowance. Observed32 compile:7.215178 child+.070629059 parent=7.285807059CPU seconds, peak205636KiB. Combined with the64 compilation7.129891665, the shared total is14.415698724 of30. Parent memory is lowered only after fork, preserving the compiler's512MiB hard limit. There is no compile retry or reset.

This package preserves all64 outputs, historical failed scalar accounting, earlier physical fixtures, accepted intervals and source manifests. Root documents and remote state are unchanged. Independent physical/scalar review is required before promoting the new kappa pair.
