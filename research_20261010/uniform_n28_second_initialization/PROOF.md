# n28 direct coverage bridge and initialization diagnostic

2026-10-10 22:25 EDT / 2026-10-11 02:25 UTC. Exact producer result; independent review pending.

## Positive statement, carefully scoped

Uniform periodic spin-one Heisenberg chain, bilinear coupling1, shift700741/500000, beta49/4. A fresh exact D26 MPS56 anchor and the same independently validated18 thermal inputs certify unique ground state and gap>=179/10000=.0179 for EVERY integer28<=L<=56. Combining this window with the separately frozen n30 bootstrap certificate proves the same bound for every integerL>=28.

The bootstrap initialization remains30. This package lowers the coverage onset to28; it does NOT certify n28 bootstrap startup. The older stronger .0245 from32 and .0248 from34 remain valid and are not overwritten by the wider-range .0179 claim. The n30 dependency manifest is fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84.

## Exact direct certificate

certify.py copies the signed-unit-atom construction of the frozen n30/32/34 package, using its exact signed-sector moment intervals and N28 polynomial majorant. The length56 upper trace uses exact rational-power packing, not a72-site anchor or an unproved long trace. Fresh N0_56>0 and H0_56/N0_56+56a<0 give Z56(beta)>1 for all beta>0. The same packing contradiction forces a positive J atom above ell and bounds its residual J twelfth mass. Thus it gives canonical S(28,beta0),T(56,beta0), followed by the independently reviewed signed all-integer window lemma.

The first lower thermal purity is C=.5800209325816545 (display only). For g=.0179 the exact margin C-exp(beta*g)(1-C)=.05707406328829727 is positive. The lemma applies to every integer28..56, including odd lengths; no positivity of each transfer eigenvalue is assumed. The union[28,56] and[30,infinity) has no missing integers. Exact fractions and margins are in certificate.json.

## What failed, and what this does not prove

The direct beta49/4 canonical recurrence using these specific seed lower bounds cannot certify its third integer window: at round2 the lower C=.4439946414447402 is below1/2, even when the requested gap is zero. This is a failure of this bound/continuation attempt, not an upper bound on actual physical purity, a universal obstruction, or a minimum-seed theorem. The first two states/windows, exact failing endpoint and original seed data are recorded.

cooling_pilot.py additionally considers the finite grid ell in{12,16,18,20,22,24,26,28}, cooling r=1.00..3.00 in.01 increments. Its generic two-sector cooled mass bounds are D=(Jell+3Nell)^r, E=Jell^r and tau=(D+3E)/4. This uses Gibbs cooling of the identity and three equivalent pi seams; at even ell, physical pi trace Jell-Nell<=Jell. For a unique leading trivial atom t, residual exponent-q tail is bounded by max{3((D-t)/3)^q,(tau-t)^q+3((D-tau)/3)^q}. Initial forcing and subsequent tail updates are floating proposals, not exact certificates.1021 candidates pass its preliminary forcing geometry; none reaches successful continuation. The largest sampled initial joint purity occurs at ell20,r1 (beta49/4), S≈.85950865,T≈.85904051 and fails its next window. This generic cooled construction is weaker at r1 than the directly retained signed-sector construction, and this finite grid is not a proof about all temperatures, base moments, adaptive schemes or improved majorants. No new thermal-temperature matrix was computed.

No n26 attempt is included. A finer temperature search, a different exact majorant or stronger compatible base data might change initialization feasibility. There is no demonstrated need to enlarge D or start new thermal production merely because this attempt misses startup.

## Resource and provenance

The extra unchanged D26 length56 contraction used CPU5,9.86936CPU seconds and32996KiB, hard100MiB/60CPU-second process limits. Including prior60/64/68 producer anchors, cumulative contraction cost34.74137CPU seconds remains below the original60-second budget. The actual executable is the frozen sibling contract_ground binary, identical source copied here. Physical block interpretation is inherited from independent original D26 audits; the new56 contraction requires separate independent replay before promotion.

The exact direct/failed-continuation replay uses CPU2,120CPU seconds/256MiB hard limits and completed in2.13CPU seconds/~11MiB. Cooling is a subsecond floating scan. No ED, tensor optimization, new thermal campaign or remote changes. Reproduce with python certify.py and optional python cooling_pilot.py. All accepted sibling files remain unchanged. This package's own INPUT_SHA256.json and manifest freeze its dependencies, source and outputs.
