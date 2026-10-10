# Research restart — 10 October 2026

## Authorization and scope
The user resumed research from GitHub and requested ongoing main updates and reports every five hours. The confirmed stop time is 13 October 2026, 20:00 America/New_York (14 October 00:00 UTC). A later pause supersedes this schedule.

Baseline: main commit 6be889a30f642bde77fb89af75b3a7379615bed1. GitHub AGENTS.md, README and historical pause records were read. The exported working tree passed all 1,149 original manifest hashes. Historical checkpoint files remain unchanged.

## Active work
1. Independently reconstruct stronger alternating spin-1 chain certificates at g=0.1, 0.125, 0.15. Verify exact local forms, full sparse residuals, completeness and finite-size bridges.
2. Independently reconstruct optimized ordinary-bilayer g=0.01 and g=0.02 inputs and recursion, including finite-size interpolation and short-size bounds.
3. Independently certify the fully frustrated J=0.3 reference with unequal straight/cross couplings, initially epsilon=0.005. Check occupancy counting, star inequalities, exact residuals and all-size scope.
4. Prove and numerically validate a full-low-band residual/completeness method, targeting the ordinary-bilayer g=0.03 ground-only-tail obstruction.

Save new scripts, exact results and reviews in the corresponding subdirectories. Keep rigorous proofs, exact arithmetic, independent checks, floating benchmarks and unverified candidates explicitly separate.

## Resource and verification policy
Use the available cloud filesystem and computation environment. There is no authorized desktop executor or saved cloud coding environment in the current environment catalog. Limit each numerical lane to two CPU cores and about 2 GB RAM, BLAS threads one. Avoid duplicate long runs. Estimate cost and retain checkpoints before extending calculations.

Each published result must state Hamiltonian, normalization, parameters, boundary multiplicities, integer-size scope, full Hilbert dimension, trial dimension, residual/tail certification, executable reproduction command and independent audit status. Do not call a sufficient tested parameter value a maximum.

## Reports and end checkpoint
Regular reports begin 10 October 18:15 EDT and recur every five hours through 13 October 16:15 EDT. At 20:00 EDT on 13 October stop computations, save reproducible results and partial work, update main and report remaining tasks. New work after this deadline requires a further user request.

## Milestone update — 13:46 EDT / 17:46 UTC

The initial three independent audits and all-size bridges are complete. The ordinary bilayer g=.03 now passes the new full-low-band and number-sector-tail route, with independently reviewed all-size gap .009195338283. Stronger chain points through g=.16125 and the specified-method obstruction at .1615 are audited. The FF one-product-state interval through epsilon=.00475 is certified.

Current priorities: larger-seed exact ground moments and translated low band; independent verification of later scalar improvements; interval certificates beyond the existing FF continuum range; bounded spin2 heat benchmarks and error proof. Completed physical audits should be reused rather than rerun without a change. Progress and caveats remain in each result directory and CURRENT_STATUS.json.

## Milestone update — 14:10 EDT / 18:10 UTC

The larger-seed 4x4/8x4/8x8 ordinary-bilayer certificates at g=.03/.04/.05 and all-size bridges passed independent reconstruction. The complete 193-state low band and 29-dimensional ground search fit the 128-spin largest seed without full diagonalization. The FF continuous interval now reaches epsilon=.00855 with independent exact endpoint, residual, tail and finite-window verification.

Spin2 kernels passed independent L3/L4 and exact-error audits, but full L10 traces cost roughly 847–1034 core-hours and the current scalar startup screen is unsuccessful. Do not start that campaign before obtaining a viable scalar route and an explicit affordable budget.

The simplified inverse-moment/sector-Temple variant has also passed independent all-size review, yielding .282017228092/.180632156388/.104475599844.

Next: derive practical trial-size/seed-size acceptance and exclusion criteria, independently audit small-seed all-temperature obstructions, and test g=.06 with reused moments before planning a second dressed triplet layer. Keep new work in separate directories from frozen inputs.

## Milestone update — 14:24 EDT / 18:24 UTC

The g=.06 temperature-first bootstrap, rigorously transported to the canonical staircase, passes independent physical, exact arithmetic and all-size review with gap .099555868340. No larger search space was needed. Practical trial-size budgets and fixed-six-vector residual floors are independently accepted. At .04/.05 the fixed canonical small-seed ladder is independently excluded at every beta, even with exact physical traces.

Next: independently verify the new bosonic pair-creation tail estimate, test all-order extensions of the small-seed obstruction, and verify the spin2 finite-moment counterexample before considering any expensive heat inputs. Second dressed-triplet support expansion remains deferred while cheaper exact improvements are assessed.

## Milestone update — 14:40 EDT / 18:40 UTC

Bosonic pair-creation and stable quadratic-reference proofs passed independent audit. The global recombination review verifies 36 patch records and 35 successful certificates, yielding .318085460990/.235117964607/.171822115684/.103487228301 at g=.03/.04/.05/.06 for every integer L>=2. The same-order baseline comparison isolates the effect of tail tightening from order transport. All six fixed small-seed orders are now independently excluded at every beta for .04/.05.

Next priorities: prove and independently verify the reduced-input txy implementation in which the largest trace is numerator-only and needs only a Rayleigh lower trace certificate; compare its one-state numerator with the existing full band; test temperature-first chain candidates with saved physical inputs; perform bounded .07/.08/.10 bilayer tests. Spin2 full traces remain deferred while ratio startup is unresolved.

## Milestone update — 15:10 EDT / 19:10 UTC

The ordinary-bilayer entire interval 0<=g<=.07 passed independent exact physical-moment, polynomial, tail, scalar and all-integer-size review, with uniform gap .001945771244. The chain temperature-first method now covers g=.175 with gap .006791087005 for all M>=2. The reduced-largest-input proof passed strict minimal-data and poisoned-extra-file tests: the earlier one-ground-numerator version only needs largest G/K, with no largest residual or completeness calculation.

Next: finish independent full-ground-pencil and combined filtered-numerator scalar reviews; the combined .08 point is a candidate until its all-size seal. Extend the continuous interval with fixed polynomial moment witnesses. Inspect analogous chain filters using saved inputs before any large support expansion. Preserve the cheaper G/K-only path separately because the optional filter consumes existing higher moments. Spin2 full traces and second dressed-triplet large supports remain deferred.

## Stage 6 independent acceptance

Full-ground moment pencils, implicit Rayleigh filters and all-size recombination have passed independent reviews. The discrete ordinary-bilayer certificate reaches g=.08 with gap .023243965748; dropping largest odd numerator terms gives .023241913957. The continuous interval reaches .078 with uniform .001945771244. All producer snapshots remain immutable; the separate review reports determine the accepted status.

Next: exploit rigorously preserved joint trace ratios when transporting direction orders, compare repeated time-first cycles, and test .09 using analytically justified coupling-polynomial moments. The analogous chain joint-ratio extension is under exact verification. Retain the previously certified results while these proposals are reviewed. No expensive full spin2 heat-trace campaign or second dressed-triplet support expansion has begun.

## Milestone update — 2026-10-10 17:08 EDT / 2026-10-10 21:08 UTC

Stage 6 is published and remotely verified at commit 00593ba445c26b1da625c9afe618e85a2550f70e. All 1,435 snapshot entries match, with 3,390 outside files preserved. The following newer inputs have independently passed review and are being prepared for the next publication.

The ordinary bilayer now has an entire [0,.085] certificate with gap .001945771244 for every integer L≥2. The ground-only part reaches .082. The final pieces add 49/97 denominator low states with total trial dimensions 59/125. The largest physical seed remains 128 spins with one retained numerator and search dimension at most 30. The discrete .085 point gives .027887084487 after repeated time-first cycles, with every earlier size window kept.

The alternating spin-1 chain reaches g=.2 with gap .043446395688 for every integer M≥2. A 13-dimensional bare small-patch comparison and full residual Gram avoid requiring an isolated entire low band. The weighted dimer complement includes quintets at energy 3.

The independently checked nonperturbative assessment separates the uniform-Heisenberg D26 recipe limitations from the AKLT parent reference. AKLT has a D=2 exact state and local 81-dimensional positivity certificate, yielding gap≥.1 at every periodic L≥5 under its projector normalization. Its current thermal-transfer sufficient condition fails, so this reference is not presented as a thermal-bootstrap extension.

Next priorities are the exact higher numerator moment and 43-dimensional search at g=.09, refined smallest-seed joint-constraint obstructions, and few-state seed-size screens for uniform spin-1 at n=10,12. Each has a separate producer and independent review. No full spin-2 campaign or q≥8 physical expansion is scheduled. Ordinary authorized main synchronization continues without asking again for each batch.
