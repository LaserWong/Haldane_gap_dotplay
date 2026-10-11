# Independent review: second-moment robustness intervals

2026-10-11 04:22 UTC / 2026-10-11 00:22 America/New_York (EDT).

## Verdict

ACCEPTED, for the periodic spin-one chain H_M(g) = Σ_j [h_(2j−1) + g h_(2j)], physical L = 2M and every integer M ≥ 2. The designated first bond coefficient is one. Each of the following closed coupling intervals has a unique finite-volume ground state and the stated physical-unit spectral gap:

- |eta| ≤ 6/112525: gap ≥ 1/50 = .020.
- |eta| ≤ 49/450075: gap ≥ 3/200 = .015.
- |eta| ≤ 37/225025: gap ≥ 1/100 = .010.
- |eta| ≤ 99/450025: gap ≥ 1/200 = .005.

Here eta = (1−g)/(1+g), so the exact interval endpoints are [(1−r)/(1+r),(1+r)/(1−r)]. Their reduced rational forms are recorded in results.json. No odd physical-ring, optimal phase boundary or actual-gap estimate is claimed.

Producer manifest bcc9601beaaf7c76557df759a0166a5f3eede1aa5287936b7bd7effaf6d222fb and the independently accepted observable manifest 8d26c955fb5500893be65dbbc6e639a86b230d299c9b59ed201a6f89728875ee are verified. Prior seals are preserved. The review imports no producer implementation and performs no new physical contraction.

## Seed comparison and units

Write H_M(g) = c(H0 + eta B), c = (1+g)/2 = 1/(1+eta). The unchanged β0 = 49/4 therefore corresponds to actual physical inverse temperature τ0 = β0/c, bounded above by β0(1+r) throughout the closed interval. The shift per physical site is c·700741/500000; linear shifts cancel from purity ratios.

The joint observable review has independently established κ32 ≤ 17/125 and κ64 ≤ 157/1000 for the actual uniform Gibbs states. These are not trial-state expectations. Translation reverses B while fixing the uniform Gibbs state. Together with ||B_L|| ≤ 3L/2, the scalar cosh bound and Golden–Thompson give

    1 ≤ Z_eta,L(β0)/Z_0,L(β0) ≤ F_L,
    F_L = 1 + κL[cosh(β0·3Lr/2)−1].

The lower comparison also holds at 2β0, without a second-moment estimate at that temperature. Consequently the accepted uniform n32 seed transports to

    S_eta ≥ S0/F32²,       T_eta ≥ T0/F64².

The checker verifies both factors, their length-specific κ values, the loss directions and the accepted S0/T0/negative total-Rayleigh anchor. It never multiplies the already-total H64 numerator by 64 again. The retained MPS is one D26 vector and is unchanged.

## All integer cell sizes

The independently accepted positive-cell construction represents the alternating physical partition function as Tr[(A_g A_g*)^M], with A_g Hilbert–Schmidt between the two appropriate bond-history spaces. All present g are positive. This existing analytic structural result is inherited with its manifest; the present audit does not replace it by an invalid product-of-self-adjoint-operators assertion.

For s,t lower bounds at a cell seed n, positivity and Schatten norm interpolation imply, for every integer n ≤ M ≤ 2n,

    purity(M,τ) ≥ min(s sqrt(t), t) = C.

The checker reconstructs this bound independently and checks C > 1/2 and C > exp[β(1+r)D](1−C). The largest Gibbs weight is at least C, so the latter inequality gives a unique ground state and gap greater than D across the complete integer-cell window. It includes odd cell sizes.

It then checks each exact directed update, including use of the newly updated spatial value in the thermal step:

    s_new = G(s²t),    t_new = G(t²s_new),
    G(x) = 1−(1−x)²/(2x²).

Every physical/cell coordinate, doubled temperature, full window, recorded rational endpoint and margin is checked. At u = max(1−s,1−t) ≤ .01, the verified recurrence constants give u_new ≤ 5u². The interpolation purity is at least 1−3u/2 and its excited/ground ratio at most 2u. The strict terminal inequality 5u exp[β(1+r)D] < 1 therefore closes all subsequent doubling windows. The four terminal cell sizes are 256, 256, 512 and 512; there are 22 explicitly checked finite bootstrap windows.

## Closed finite bridge, including its zero margin

The independent uniform theorem supplies gap ≥ 31/1250 for every integer physical L ≥ 2. Weyl's inequality and ||B_L|| ≤ 3L/2 give, only for the finite missing lengths 4,6,…,30,

    gap(H_M(g)) ≥ [(31/1250)−3Lr]/(1+r)
                 ≥ [(31/1250)−90r]/(1+r).

Each chosen radius is exactly [(31/1250)−D]/(90+D). Thus the last displayed lower bound equals D and the coarse bridge margin is exactly zero. This is valid: the claim is gap ≥ D, and D is strictly positive, so uniqueness follows. Requiring a strictly positive margin beyond D here would incorrectly reject the legitimate closed endpoint. Every infinite-bootstrap margin is strictly positive.

The bridge covers cells 2 through 15; the bootstrap starts at cell16. Their union and the overlapping doubled windows cover every integer M ≥ 2. This is the maximal radius for this particular coarse bridge, not for the available length-specific finite evidence or the physical model.

## Independent arithmetic and resources

The checker uses a 700-bit dyadic enclosure grid, positive rational Taylor sums with a rigorous geometric tail, reciprocal bounds for negative exponentials, and integer-square-root checks. This differs from the producer's 160-place decimal enclosures. Producer state rounding at the advertised decimal grid is checked exactly, while all analytic inequalities are verified against the reviewer's finer bounds.

Twelve corruptions are rejected, covering omitted trace losses, swapped κ labels, wrong coupling endpoints, cell/physical confusion, missing temperature scaling, missing windows, inflated sequential updates, terminal scale, missing finite cell15 and an inflated bridge bound.

One numerical run passed: wait4 .318928 CPU seconds plus .071395445 launcher seconds; peak 15544 KiB. Hard caps were 4 child CPU seconds plus 1 parent second, 256 MiB, CPU5, 90-second whole-session watchdog, active aggregate CPU polling, verified post-exec signal/affinity/resource guards and parent-death SIGKILL. No guard fired, no descendants remained, and no retry occurred. This charge remains within the parent's original remaining review budget. Exact sources, logs, results, input pins and manifest are retained separately from the observable seal.
