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

## Milestone update — 2026-10-10 17:28 EDT / 21:28 UTC

Stage 7 is remotely verified at fb38f57548c86d9dda19450e68cbbedbafd6765a. All 805 new or changed entries match and 4,822 pre-existing paths outside the inventory are preserved.

Exact third-moment contraction and a 43-dimensional largest search with one retained numerator state certify g=.09 with gap .027330086079 for all integer L≥2. Seven new closed pieces extend the whole continuous interval to [0,.09], preserving uniform gap .001945771244. The physical contractions, counted denominator spectra, directed scalar replay and all finite-size windows have separate independent seals.

Uniform-chain fixed D26 screens now have independently accepted all-temperature obstructions at n=6,8,10,12,14,16,20 under their explicitly specified recipes. Compact exact excited-state contractions avoid full physical support expansion at n=24. The three-state n=24 screen leaves the closed temperature window [13/2,45/4]; this is not a successful seed certificate. A longitudinal fourth state and displacement-resolved momentum states are under separate investigation. The alternating-chain 67-dimensional small reference gives new candidates above g=.2, pending independent scalar review.

Next: publish the stable stage 8 scope, finish independent review of the stronger chain comparison, tighten the n=24 necessary screen with more orthogonal low-energy witnesses, and identify the trace-upper information required for a successful nonperturbative seed. Do not substitute a bounded numerical scan for an all-temperature exclusion. No full spin-2 spectral campaign is scheduled.

## Milestone update — 2026-10-10 17:46 EDT / 21:46 UTC

Stage 8 is published and verified at 609894b496a4deb519eaa2df1507e69f3aec6b67. All 425 snapshot files match remote hashes and 5,624 outside paths remain unchanged. The 1D-to-2D explanation is published with explicit startup, transfer, partial-data and omitted-spectrum conditions.

The alternating-chain 67-dimensional small reference has independent all-size certificates at g=.21/.22/.225, with bounds .101607534008/.065580452251/.045509923956. The maximum physical seed remains M=8 and its numerator input is unchanged. Larger-reference g=.25 diagnostics have separate pending review and are not a new gap certificate.

At n=24 in the uniform spin-1 chain, exact displacement contractions and certified Fourier algebra give 70 orthogonal trial states with bond dimension at most 52. Total-spin singlet structure is proved at this finite size from an exact zero norm, and normalized lowering supplies all spin components. The strongest accepted fixed-recipe necessary screen still leaves beta in [539/64,339/32]. A compact two-vector current-operator extension is being benchmarked independently of these frozen results.

The g=.1 bilayer diagnostic is independently accepted as a scoped input-sensitivity analysis. Available moments sharpen ground lower endpoints without reaching startup on the tested grid. The 8×4 denominator remains the tested bottleneck. An exact hard-core pair commutator may supply the complete new residual without enumerating q=8 supports; its local fixtures have passed and the separate physical producer/reviewer are active. This is not yet a g=.1 certificate.

## Milestone update — 2026-10-10 18:00 EDT / 22:00 UTC

Stage 9 is published at 46f6c7348d7fb1bc67ba05991f10988bee7dd155; all 391 entries verified and 6046 outside paths preserved. New independently accepted bilayer residual data give the g=.1 point bound .038976038275 for all integer L≥2. A complete q=8 norm is obtained exactly from q≤6 contractions using the signed hard-core commutator. No term is discarded. The new 8×4 ground search is 43-dimensional; total denominator trial dimensions are 59/139 and retained bands remain 49/97.

Ten independently reviewed closed intervals extend the full range to [0,.1], preserving uniform gap .001945771244 over 66 pieces. Final interval review manifest is d6eb3e4ce912086fe66dc1eb2917c3ae7381bc6a527a939b99229b97b863f3e5.

The chain rank 195 comparison and denominator-independent obstruction at g=.25 are independently accepted within the specified old M8 span and first-window recipe. Its exact necessary numerator target guides new finite-dimensional searches; it is not a general minimum-size or gaplessness theorem. Uniform-chain pi-current contractions are checkpointed and under independent algebra/fixture review, with a measured one-core computational cap.

Next: publish the stable stage 10 scope and scheduled 22:15 UTC report, continue the two pending numerator/current refinements, and independently audit each new claim before inclusion. The research stopping time remains 2026-10-13 20:00 New York.

## Stage 11 milestone — 2026-10-10 18:25 EDT / 2026-10-10 22:25 UTC

Stage 10 is remotely verified at f89164be50de9b5e868d08b80bd178eaca4b9a1a. The scheduled report was sent at 18:15:12 EDT / 22:15:12 UTC; the next is 23:15 EDT / 03:15 UTC on October 11. This is a local stage11 preparation record, not a remote publication claim.

The [direct integer-window audit](integer_window_refinement_review/PROOF.md) accepts alternating-chain g=.21/.22/.225 gaps .107424972/.071581253/.051807500 for all integer M>=2. At g=.25 the accepted .01 gap covers only M=2..16. Its exact lemma uses even n, a<=T(n,beta), b<=S(n,2beta), b>1/2, and w=(1+sqrt(2b-1))/2: odd M uses a^(M/n)[w^(M/n)-(1-w)^(M/n)], even M uses (aw)^(M/n), giving a²sqrt(2b-1) on n<=M<=2n. It requires the reviewed self-adjoint Hilbert–Schmidt transfer and positivity of all integer physical traces; no size-purity monotonicity or time/space relabeling. The [producer prose erratum](integer_window_refinement_review/PRODUCER_PROSE_ERRATUM.json) changes the stated purity from >.542 to >.54167130 without changing numerical certificates or frozen files.

The [prior rank4](chain_m8_numerator_review/README.md) and [new rank9/13/17 numerator audits](chain_numerator_pair_block_review/README.md) accept exact physical Rayleigh/rank calculations and only their scoped old-route exclusions. Inherited rounded psi/u are not exact singlets or translation/reflection eigenvectors. Exact symmetry applies only to the five added pair/vacuum directions and pair-derived H descendants. The explicit [scope erratum](chain_numerator_pair_block_review/SYMMETRY_SCOPE_ERRATUM.md) confirms that existing full-space denominator and arbitrary-vector Rayleigh certificates remain valid.

[Uniform transfer moments](uniform_transfer_moment_review/README.md) at beta=21/2 and energy shift a=700741/500000, conditional on inherited physical heat certificates and self-adjoint transfer identification, improve the normalized trace caps to 1.238492320537 and 1.131484383792, with no new gap. The [current MPS review](mps_commutator_review/REVIEW.md) is fully PASS, including all 74 independently contracted integers and trial-energy difference .4238202243082572. This is not a physical excitation gap. Its 70/73-state old-recipe exclusions, [n18/n22 completion](mps_seed_even_completion_review/REVIEW.md), and [direct-window relaxed continuation audit](mps_direct_window_review/REVIEW.md) supersede old n24 unresolved windows. Every even n6..24 is individually covered for the specified G initialization, whole-cycle delays and same-base sufficient closure or joint-aware canonical continuation, even with finite bridges granted free. No exact physical-purity bound, arbitrary adaptive switching exclusion, all-method minimum seed, or physical gaplessness is claimed.

The ordinary-bilayer entire [0,.1] bound .001945771244 and discrete .1 bound .038976038275 are unchanged. Earlier g=.1 diagnostic failure records are historical and superseded by those accepted proofs; original files remain untouched.

Next priorities:
1. The [cooled uniform-chain audit](uniform_cooled_seed_review/REVIEW.md) has now reached final independent acceptance (18:27 EDT / 22:27 UTC): n60 gap .0102 for every integer L>=60, n56 gap .0068 for L>=56, n54 gap .0025 for L>=54, each with a unique ground state. Review manifest: a5b5f3b35d67f69f555455143e8e5c70beaff46aba2469705c3e22eb7c00a5d7. The nine heat traces and self-adjoint transfer identity are inherited audited inputs, not freshly recomputed. D26 matrices and exact contractions at 104/108/112/120 were independently reconstructed; all finite integer windows and asymptotic closures pass. n60 improves the existing size, n56 uses original quadratic-tail structure, n54 adds generalized sector powers. Further work must separately review any smaller-size bridge; no claim below L54 or of a minimum seed, and no no-go theorem from failed n52 floating tests.
2. Test the certified rank17 chain numerator with the new direct integer-window route, within bounded computation. A g=.25 all-size result still needs every subsequent integer window and asymptotic closure.
3. Reuse accepted bilayer inputs for scoped stronger-coupling diagnostics. Keep spin2 full traces and large physical-support expansion deferred without a viable affordable route.
4. Prepare the stage11 overview and publication, retaining all previous rows and clearly separating finite-size results, exact trial calculations, recipe exclusions and unaccepted candidates.

Strict stop: 2026-10-13 20:00 America/New_York (EDT), 2026-10-14 00:00 UTC. Stop research computation and save final reproducible/partial checkpoints then; a later pause takes precedence.

Stage 11 reproduction transport: [lossless evidence materialization](../reproducibility/stage11_exact_evidence/README.md) maps 18 raw paths/nine unique contents to 21 gzip parts. From the repository root run `python3 reproducibility/stage11_exact_evidence/materialize.py --repo-root .` before original sealed-source checks or reproduction. The transport restores original bytes, paths and modes; producer/review seals remain unchanged. Clean hydration, original-seal replay, idempotence and corruption/safety tests passed.

Stage 11 overview frozen at 22:32:43 UTC: [overview_stage11](overview_stage11/README.md), manifest 46691981a4e687d26cb5cff86b63c1355dd695f2c8957394d7b842b01576be7a. All 225 prior all-size rows are preserved within 228 rows; the finite g=.25 record and three uniform-chain large-size ranges remain separate. Final root status refresh: 2026-10-10 18:34 EDT / 2026-10-10 22:34 UTC. This is local preparation; remote publication is not asserted.

The stage11 post-freeze read-only reproduction completed successfully at 22:34 UTC with its manifest unchanged. Root files are ready for publication QA; no remote publication is claimed here.

## Stage 12 milestone — 2026-10-10 18:44 EDT / 22:44 UTC

Stage 11 was published and remotely verified at commit 897e07867c612bd3222e8f71d3b15122cd7c733e, tree fb670620513109ec4d61a6dea06b52460c20269d. The user was notified at 22:43:20 UTC; the next regular report remains 03:15 UTC on October 11. This stage 12 section is local preparation, not a publication claim.

The [n52 uniform-chain review](uniform_seed_frontier_review/REVIEW.md), manifest b71dfa41a851c509ec5bad6382f458ad6f51531934bbd90143ee9162779cbaf2, accepts gap>=.0038 and a unique ground state for every integer L>=52 under unit Heisenberg coupling. Exact Hermite majorants improve the envelope while reusing the same nine certified thermal inputs, accepted MPS104 and self-adjoint transfer premises; no new heat-trace job or physical contraction is implied. All early signed-integer windows and asymptotic closure pass. Preserve the stronger .0068 at L>=56 and .0102 at L>=60; .0025 at L>=54 remains a weaker historical result. No below52 or minimum-seed conclusion.

The [2D direct-window review](bilayer_direct_window_review/PROOF.md), manifest 8e2726b4925b752fed9789dc43b3486229a626e4d7d07b45c1d6b5171d23f8c7, improves the ordinary-bilayer g=.1 point to .055807148827 for all integer square L>=2. The proper staircase a<=T(n,m;beta), b<=Sx(n,m;2beta), c<=Sy(2n,m;2beta) yields the gated rectangle lower bound a^4(2b sqrt(c)-1)sqrt(2b²sqrt(2c-1)-1). Both transfer directions, odd transverse widths, every preceding finite box, short sides and asymptotic closure are checked. It neither swaps temperature labels nor asserts all aspect ratios from dyadic boxes.

The [66-piece continuation](bilayer_direct_window_continuation_review/README.md), manifest c9dadb17430a3523cda109599f3025ff62c7b9ebebacc2b9eb48acce2381e977, improves the whole [0,.1] lower bound to .004499695659. The [new frontier-point audit](bilayer_frontier_above_010_review/README.md), manifest d101b554ea00c044e148031ec4d073d10f6f757b78a019e5bc6502a67e086d05, certifies .1001/.1005/.101/.1015/.102 with gaps .054499712024/.049244008353/.040917096762/.029199965244/.016509932002. Frozen fixed_center metadata has an explicit erratum: the actual exact reconstruction is at z=.1. These point claims alone do not certify a continuous interval or the wider physical legality domain.

The final [eight-piece interval extension](bilayer_frontier_interval_0102_review/README.md), manifest 45d651b0f68b840ed2c7a42978acd975d7789b69ad75acd3b4c21a9b74d2a7ed, accepts every real g in [.1,.102] with gap>=.013574634391 and the combined 74-piece range [0,.102] with gap>=.004499695659, for every integer square L>=2, unique ground state. Its 16 endpoints, 384 odd-mode checks, 68 finite windows, all short-size bounds and asymptotic witnesses pass. Explicit interior convexity/concavity replaces any gap-monotonicity assumption.

[Original-source scope](uniform_source_scope_review/SOURCE_SCOPE.md) and [license/attribution](uniform_source_license_supplement/README.md) are published supplements. The original paper proves gap>(4/105)log(80/79) for even L>=60 and gap>log(20)/784 for even L>=2304. The new .0102 lower bound is about 21.2858 and 2.6694 times those constants on the respective common even scopes, not a ratio of physical gaps. Its transfer identity covers every integer n>=4, permitting the separately proved signed odd extension; do not attribute an odd-length gap theorem or n=2,3 transfer assertion to that source. The later archived .005908566393 for L>=1920 is not the original theorem.

Next: prepare and verify overview_stage 12, then publication QA; keep the new stronger ranges and inherited source boundaries explicit. Further smaller-seed or stronger-coupling proposals need separate exact review. Do not rerun accepted physical inputs without a reason. Strict research stop remains October 13 20:00 EDT / October 14 00:00 UTC; next regular report remains October 11 03:15UTC.

Stage 12 [overview](overview_stage12/README.md) frozen at 22:48:34 UTC, manifest 39c5b539217441e82c36186411f6604cb2ff260a9ebac47962fb4a0b8c203803, with 61 files. It preserves the prior 228 all-size records within 311 records, with four separate uniform-chain large-size records and one finite-chain record. The current coupling cover has 74 closed pieces through .102. Post-freeze read-only replay passed at 22:50:31 UTC with all sealed files unchanged; no remote publication is claimed.

Stage 12 root files finalized at 2026-10-10 18:50 EDT / 2026-10-10 22:50 UTC, after successful overview replay, for publication QA.

## Stage 13 milestone — 2026-10-10 19:11 EDT / 23:11 UTC

Stage 12 is remotely verified at 340bef8be2de4649e8e6271bdbe6d70c063dcdae. The latest publication notice was 22:59:06 UTC; the scheduled report remains October 11 03:15 UTC. Stage 13 is local preparation until separately published.

The [actual g=.105 point review](bilayer_g0105_actual_point_review/PROOF.md), manifest 02cdd689b9bf4608b540a95316672708eb4691b56057ad8fb23082a930185c12, accepts gap>=.031673112867 and a unique ground state for all integer periodic squares L>=2. Its [16D 4×4](bilayer_16d_4x4_residual_g0105_review/PROOF.md) and [optimized 43D 8×4](bilayer_optimized_residual_g0105_review/PROOF.md) physical audits independently reconstruct complete residuals. Ground search dimensions 16/43, total trial dimensions 64/139 and retained low-band counts 49/97 differ; the largest 43D search retains one numerator term in physical dimension 2^128. These physical reviews alone do not prove an all-size gap; the actual point replay closes every window and uses no assumed target residual.

[Seed-error budgets](bilayer_seed_error_budget_review/PROOF.md) concern chosen sufficient allocations and precise saved-subspace/Temple restrictions. They are not necessary conditions or universal obstructions. The actual 8×4 variance exceeds its selected component target yet the complete path succeeds. The selected g=.11 joint allocation is physically inconsistent and discarded.

[Uniform moment optimality](uniform_moment_optimality_review/REVIEW.md) gives abstract fixed-moment information limits and integer-count spectra satisfying the input intervals and seam positivity; it does not provide quantum or cross-temperature realization, a physical gap or seed impossibility theorem. [MPS96/100 anchors](uniform_anchor96_100_review/REVIEW.md) separately accept exact negative shifted total Rayleigh quotients only, not thermal upper bounds or startup.

[Fixed n48/n50 grammar exclusions](uniform_seed_recipe_minimum_review/REVIEW.md), manifest ff6500e7dacf713d601053c1abcaa0bf1d974bce1c895e96f1c1f2e62d923c56, cover only those two sizes, all 41 allowed even bases and all real cooling ratios r>=1. Fixed nodes/moments/caps, Hermite/packing and one fixed accepted MPS anchor feed canonical staggered sequential-G continuation. All 332 closed boxes fail by a genuine nonpositive update; analytic cold rays and ideal unrounded evaluation are included. No alternative initialization, time-first delay, adaptive permutation, reinitialization or smaller n<48 is included. Failure at 48/50 plus success at 52 does not prove 52 minimal, even in this grammar. Distinguish finite-size coverage onset from bootstrap initialization seed.

The user clarified at 23:00:56 UTC that the original paper already uses certified matrix-polynomial thermal traces, not a full-ED premise. Keep that explicit in comparisons: these refinements reuse the same nine certified heat inputs and improve envelopes, anchors, recurrence or bridges. Ongoing adaptive initialization and D26 tensor feasibility are outside this stage's accepted scope.

Next: the six-interval extension is now finally accepted as recorded below; finish stage 13 overview/reproduction and publication QA. Any new lower-size finite bridge requires an independent seal and must not be mislabeled as a new bootstrap initialization. Deadline remains October 13 20:00 America/New_York / October 14 00:00 UTC; regular report remains October 11 03:15 UTC.

The final [six-interval extension review](bilayer_interval_0102_0105_review/PROOF.md), manifest 0c19177fdb91be54ba1892e5e3960e18a90e0ace9f11018018445368333eea9d, passed clean reproduction. Every real g in [.102,.105] has gap>=.017785998829; the combined 80-piece interval [0,.105] has gap>=.004499695659, for every integer square L>=2 with a unique ground state. Complete variance polynomials, 12 physical endpoints, 288 odd-mode checks and 50 finite windows are independently verified, without physical-gap monotonicity. Counts remain 16/43 ground searches, 64/139 total trial dimensions, retained 49/97, and one largest numerator in physical dimension 2^128.

Final [uniform direct 48–96 window review](uniform_n48_direct_window_review/REVIEW.md), manifest 1f94ecf80d9674416d07b5ed47b2aa28642b62c8f235ec0a792c96c499c5ae17, accepts gap>=.0053 with a unique ground state for every integer 48<=L<=96. Together with the accepted n52 theorem this gives gap>=.0038 for every integer L>=48. The coverage onset is now 48, but bootstrap initialization remains 52; fixed n48/n50 canonical-startup exclusions remain valid. Direct inputs are T(48,21/2) and S(48,21), not the length96 thermal coordinate of canonical startup. Nine archived thermal certifications, analytic transfer identities and accepted MPS48/96 anchors remain inherited premises. No fresh contraction, provisional MPS50, adaptive startup, below48 or minimum-seed claim enters acceptance.

Original-startup comparison correction (user clarification 23:19:41 UTC): [the original initialization proof](https://github.com/openai/math/blob/main/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/build/initialization.tex) already has a second route starting at n=36, beta=49/4, with 18 I/P thermal entries at lengths 4..12, reaching n=2304, beta=784 after six rounds. The n52 startup-size improvement is relative to the original first nine-input n60 route only, not all original recipes. The stronger .0102 certified bound and current coverage onset 48 remain valid and distinct claims. Original second-input totals are available, but those thermal columns were not independently rerun for this stage; new work on them is outside this publication.

[Stage 13 overview](overview_stage13/README.md) is locally frozen with 67 files and manifest 25c5663d046405f58899a205df1edaa1bd5b3a42b327919b8c9475294a4944fa. It includes all 80 bilayer intervals, the separate finite 48–96 uniform window and composed L>=48 coverage, while retaining initialization 52. Post-freeze read-only reproduction passed at 23:21:17 UTC with all sealed files unchanged; no remote publication is asserted.

Stage 13 root files finalized at 2026-10-10 19:21 EDT / 2026-10-10 23:21 UTC after successful overview replay. No further scientific additions enter this freeze.
