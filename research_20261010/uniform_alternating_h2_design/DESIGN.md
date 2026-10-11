# Read-only assessment of H²32/64 variance refinement

2026-10-11 04:38 UTC. Design/scalar comparison only. Preserve every completed physical/interval seal and use only the accepted kappa.136/.157 and accepted intervals for Stage21. Proposed tighter kappa numbers below are producer-only until separately certified and reviewed.

## 1. Stronger ground Gibbs weight without physical work

At beta0=49/4 and shifted H'=H0+aL, a=700741/500000, let Q upper-bound Tr exp(−beta0 H'), and let mu be the exact total shifted Rayleigh quotient of the normalized accepted D26 trial. Variationally E0'<=mu, so

    p0=exp(−beta0 E0')/Z >= exp(−beta0 mu)/Q = w_R.       (1)

This is a lower bound on the actual ground Gibbs weight. It does not identify the trial with the ground state. A lower endpoint w_R>1/2 independently forces uniqueness. No factor L is applied to the already total H/N.

The existing purity argument instead gives w_P=(1+sqrt(2C−1))/2. For a one-vector numerator C≈exp(−2beta0 mu)/Q², equation(1) is essentially sqrt(C), which is larger than w_P except at C=1. The exact accepted inputs give:

| L | Previous purity weight | Rayleigh/trace weight lower, display |
|---|---|---|
|32|.9366474892930138|.9387875477507066|
|64|.9134631964156602|.9176574240821238|

The exact100-place lower endpoints are saved in DESIGN_SCALARS.json. With the existing conservative fidelity endpoints unchanged, replacing only the Gibbs weight gives kappa upper displays.13330078198858114 and.15303303567904417.

There is also cheap room in the scalar energy/gap endpoints. The same Q gives E0'>=E_lo whenever lower_exp(−beta0 E_lo)>Q. The new w_R gives finite gap>=delta whenever w_R−upper_exp(beta0 delta)(1−w_R)>0. Directed checks from the original exact fractions pass at:

    L32: E_lo=−627681/100000000, delta=1783/8000=.222875,
    L64: E_lo=−702409/100000000, delta=19681/100000=.19681.

Then e=mu−E_lo and F>=f=1−e/delta yield infidelity upper displays.02313597799061205 and.03564252859864026. With the previously contracted exact q_L=<B_L²>/(3L/2)², the sharp effect bound

    alpha <= [sqrt(f q)+sqrt((1−f)(1−q))]², f>q,
    kappa <=1−w_R+w_R alpha,

gives directed producer upper endpoints.130818393625205 and.1508597314532842. Thus the simple.131/.151 pair is available without H², subject to its own reproducible certificate/review. This note does not promote that pair or recompute an interval. The seed-loss improvement over accepted.136/.157 would be about2% in radius in the quadratic regime.

## 2. Variance-based fidelity: sharper than the basic residual bound

An exact H² contraction gives the shift-independent trial variance

    sigma² = <H0²>−<H0>² = (H2*N−H²)/N².

Let F be trial ground overlap and epsilon=1−F. The already certified energy estimate gives F>=f0>1/2. Expanding the spectral variance pairwise,

    sigma² = sum_(i<j) p_i p_j(E_i−E_j)²
           >=F(1−F)delta².

The known F>1/2 selects the small-infidelity branch. If4sigma²<=delta², then

    epsilon <= [1−sqrt(1−4sigma²/delta²)]/2.             (2)

Take the minimum with the energy-only bound e/delta. If the square-root condition fails, retain the energy bound. A simpler valid bound is epsilon<=sigma²/[delta(delta−e)], from F>=1−e/delta. Both improve on the elementary residual/Chebyshev denominator(delta−e)². No unknown E0 is substituted into a computable quantity.

The variance starts improving the refined energy-only fidelity exactly when

    sigma² < delta² epsilon0(1−epsilon0)=e(delta−e).

With the design endpoints above, the thresholds are about.0011226507986 at32 and.0013313764754 at64. These are total-energy variances, not per-site variances or variance square roots.

For scale only, the following are conditional scenarios, not measured variances:

| Assumed total variance | Resulting kappa32 upper display | Resulting kappa64 upper display |
|---|---|---|
|.001|.1265345870|.1386945665|
|.0005|.1075724880|.1190834517|
|.0001|.0874629319|.0996417281|
|.00001|.0787912087|.0920263134|

At.0001 for both lengths, seed-loss radius gains would be roughly25%; at.0005 they would be roughly12%; these are planning estimates and require an actual variance result plus a new directed bootstrap.

## 3. Best possible payoff within this effect/thermal-weight method

With only an upper bound1 for all excited-state expectations of O=B²/b², the bound1−w_R+w_R alpha has an irreducible excited-weight term. Its values1−w_R are.06121245224929344 and.08234257591787625. These are floors of this upper-bound method, not lower bounds on the actual Gibbs kappa.

Even perfect fidelity makes the sharp ground effect endpoint equal to the trial q, not zero. Since q32=.01507219528810355 and q64=.007521781460785803, the best endpoints obtainable by taking fidelity to one while retaining the current thermal weight bound are

    kappa32,ideal=1−w32+w32*q32≈.07536204150303193,
    kappa64,ideal=1−w64+w64*q64≈.08924499451768962.

This is roughly a45%/43% coefficient reduction from the accepted.136/.157. Further reduction would need additional information on excited-state B², a sharper uniform Gibbs trace/weight, or a different comparison inequality.

For a precise noncertifying seed-loss comparison, equate kappa_new[cosh(a_L r_new)−1] to kappa_old[cosh(a_L r_old)−1], where a_L=beta0*3L/2, and take the smaller r_new from L32/L64. The four current radii map in the idealized perfect-fidelity limit to:

| Current r | Loss-equivalent ideal r, display | Ratio |
|---|---|---|
|.0001291|.0001711073651|1.3253863|
|.0001816|.0002405204226|1.3244517|
|.0002159|.0002857817330|1.3236764|
|.0002368|.0003133199113|1.3231415|

These are neither new interval endpoints nor a theorem giving the global maximum radius. The actual physical inverse temperature also changes by1+r, and the accepted radii were deliberately conservative search points rather than optimal seeds. The comparison explains the approximate one-third ceiling on the H² benefit through this particular mechanism. The finite-prefix gaps have ample slack at these scales.

## 4. H² implementation and correctness plan

No new local insertion or MPS tensor is needed. Use the frozen charge blocks T,O=E_h,U=E_(h²),V=E_(h01h12+h12h01), b2_blocks.txt hash1e63ba284062733ec459fd0f2125874b561b407ef7d722897f1923336ff58581. The unchanged fixture.cpp helper, hashafaf61d76e1de0dceae377b0c61923bf3d2facf11f85a3915888a19707ad5214, already supports either sign. Set

    Kplus=[[T,O],[0,T]], Rplus_N=(Kplus^N)_upper-right,
    H2_L=L{Tr(U T^(L−2))+Tr(V T^(L−3))+Tr(Rplus_(L−3) O)}.

The adjacent sign and convolution sign are both positive. Do not merely relabel the B² output. The independently accepted fixture already matches this H² formula to full physical periodic L4/L6 vectors, including closing bonds, and the abstract binary helper to literal doubled blocks at powers0..12 for both signs. This suffices as an existing fixture premise; no larger physical Hilbert vector is needed.

Create one new wrapper with a structured length parameter32 or64, never unrestricted numeric substitution. Include the unchanged matrix kernel and preserve block sides1,8,32,80,136,162,136,80,32,8,1. Recompute N/H and require exact agreement with the accepted anchors before accepting H². Also compare the saved same-bond and adjacent scalar contributions against the corresponding B² checkpoints, since those pieces must be identical. Save H² and the exact nonnegative variance fraction, with length-labelled per-block checkpoints.

The actual current helper performs3 dense products per composition, including its first identity composition. Consequently the same work pattern uses26 dense products per charge block atL32 and32 atL64, including the two additional T products for norm/energy/local traces. Stream one block at a time. The maximum side remains162; no full676 or doubled1352 dense matrix is formed. The prior sign-independent row-norm bounds||T^64||_infinity<2^1344 and||R61||_infinity<2^1305 apply equally to the positive convolution. Ten live matrix buffers remain comfortably below256MiB by the prior design estimate.

There is no numerical cancellation problem in subtracting <H>²: the numerators are exact GMP integers. The trial space stays one vector with MPS bond dimension26; full physical dimensions are3^32 and3^64.

## 5. Proposed production budget and decision gate

The matching B² jobs measured7.744176CPU seconds/25436KiB at32 and17.185815CPU seconds/35636KiB at64. Positive-convolution integer growth has the same proven caps. A reasonable planning range is8–12CPU seconds for32 and17–25 for64, not a runtime guarantee.

Recommend a64-first gate because its denominator loss carries the larger b64 and has the tighter idealized thermal-weight floor:

1. Compile the new structured wrapper once, separately capped30CPU seconds/512MiB, preserving the old executable and source.
2. If separately authorized, run64 only under aggregate40CPU seconds(39 child+1 parent),256MiB, sole CPU4,180-second external wall limit, active CPU polling, verified postexec limits and per-block checkpoints. No automatic retry.
3. Report exact variance and its certified fidelity/kappa consequence. If variance is not below the approximately.00133138 improvement threshold, retain the free scalar improvement and reassess whether32 could materially help before spending its budget.
4. If warranted and separately authorized, run32 under aggregate20CPU seconds(19 child+1 parent),256MiB CPU4,90-second wall limit, same controls and mandatory N/H agreement. One compiled kernel suffices.

The two suggested physical caps total60CPU seconds, in addition to the separately charged compilation. Independent physical reconstruction and final scalar/interval review would require their own explicit budget. No production, compilation or new certificate search is authorized or executed by this note.

## 6. Read-only scalar cost and preservation

The design comparison read original exact fractions and used100-place directed rational exponentials/roots for the reported weight/energy/fidelity upper endpoints. Floating logarithms only proposed rational delta/E_lo candidates, each then checked by a strict directed exponential inequality. The acosh radius comparison is explicitly noncertifying.

The read-only child used1.768560CPU seconds, the parent.011453465CPU seconds, peak8028KiB, exit0 and no wall-watchdog trigger. It was bounded to4 child CPU seconds plus1 parent,256MiB CPU4, with a15-second external wall guard. This fits the7.095250644 seconds remaining after the completed interval work. The measured cumulative scalar budget is now24.684762821 of30CPU seconds; conservative full-parent accounting is28.298935 of30. No further certificate search is performed under the remainder.

DESIGN_SCALARS.json preserves the exact100-place endpoints copied from that successful read-only check, and INPUT_SHA256.json pins all referenced existing inputs. This is a bounded design note, not an independent review or replacement for any accepted result.
