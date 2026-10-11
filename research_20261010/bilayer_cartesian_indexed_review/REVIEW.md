# Independent Cartesian indexed-action review

2026-10-11 02:31 UTC / 2026-10-10 22:31 EDT.

**PASS for local Cartesian algebra, small fixtures, and the specified 512-target indexed-action sample. FAIL for the proposed 180-second production-cost gate.** No fundamental infeasibility result, full moment, or new gap claim.

Reviewed immutable source manifest: `760ab0e980cc40bd96028da1bc626353c44f463148d5dd2bc6cef81db566d1bd`, directory `../bilayer_cartesian_indexed_sample`. All manifest entries and pinned input-manifest/file hashes verified. The accepted g=11/100 8×4 witness's last fourteen coefficients exactly equal cM; the review does not substitute cR. No producer file or remote repository was changed.

## Main new independent result

All 23,040 output coefficients (3 families × 512 supports × 15 channels) from the producer's indexed_action routine equal a second direct translated-embedding action. All 512 dispersed targets are checked per family, including 285 with identically zero source m and 227 nonzero. N/F/L rule-hit totals exactly reproduce 3,228,375 / 17,729,412 / 8,691,654. Runtime 13.7927 CPU seconds, peak RSS 16,012 KiB.

The reference implementation in action.cpp reads the frozen binary matrices into separate reference blocks; retains the ordinary vacuum rows; scans every translated embedding directly; explicitly substitutes local source colors while preserving spectators; and evaluates source matching amplitudes with its own channel calculation and bounded cache. It does not use the producer's incidence selection, min-intersection deduplication, removed-vacuum treatment, vacuum polynomial, or vacindex. The producer routine's index input is reconstructed from the same immutable binary files, rather than rerunning its compiler; its index construction was reviewed against compile_index, and the relevant local matrices are independently verified below. This isolates the previously untested translated pull action without spending the budget on repeating producer compilation/fixture setup.

The producer_adapter.cpp is the frozen benchmark source with only its validate include made explicit and main renamed; this preserves indexed_action as the implementation under test. The direct reference shares matching order, read geometry/orbit data, and read coefficients as input conventions, but does not call producer analytic/source/amplitude. Matching probes and source formula are checked separately. Stored aggregate Gram checksums were not separately recomputed in this review; the stronger per-output comparison checks the actual action implementation and its second implementation, while the producer's recorded checksums remain hash-bound evidence.

## Elementary physics and complete local rules

check.py independently builds all Cartesian rung columns and the four-spin permutation Hamiltonian P_(0,2)+P_(1,3)−I. Every one of its 256 matrix entries equals the independently constructed C+C†+D table after the exact normalization factor four. Intermediate Gaussian integers are tiny and exactly represented; no floating tolerance or rounding is used. This checks ordinary bilayer physical normalization and the Cartesian phase convention.

independent.cpp imports no producer code and uses no trace-monoid normalization. It expands oriented commutators separately, evaluates unreduced words using the independent Cartesian edge table, and matches all records and omitted zeros:

- N: 134 anchored tuples, 27 blocks, 6,824 records, 1,263,448 omitted zeros, 3,104 negative coefficients
- F: 1,242 anchored tuples, 83 blocks, 263,791 records, 59,726,737 omitted zeros, 132,858 negative coefficients
- L: 1,602 anchored tuples, 83 blocks, 34,618 records, 59,955,910 omitted zeros, 14,339 negative coefficients

Total 305,233 records, 3,662,796 bytes, 121,251,328 implicit entries. Runtime 1.36707 CPU seconds and 3,328 KiB RSS.

The 32-member edge orbits and designated-anchor quotient from the accepted predecessor remain valid. Independent stabilizer enumeration gives exactly one order-four block per family and 26/82/82 trivial-stabilizer blocks. For every F/L block, the sum over its stabilizer permutations is exactly Hermitian. All 32 translated embeddings are retained; there is no support-stabilizer division and no extra 1/32. The direct action comparison exercises these ordered embeddings and vacuum coefficients on all sampled masks.

## Full small fixtures and fifteen probes

The independently implemented Cartesian C/C†/D and pair-creation actions retained from the preceding review reproduce every scalar field, all fifteen signed terms, direct and normal-ordered m3/m4, and every sector norm of both 4×2 and 5×2 fixtures. Only peak_sparse_states is excluded from scalar comparison because it is basis-dependent. The test adds its own matching enumeration and reconstructs the entire m, N m, F m and L m vectors from the fifteen probe values on every occupied support; all full-vector reconstructions pass. This is not merely agreement on fifteen test evaluations. The compiled small-vector comparison in the producer package was code-reviewed and hash-verified, rather than re-executed; independent full-vector probe tests here use direct physical nested operators.

The q10 cancellation on 4×2, nonzero q10 on 5×2, negative F, oriented cross terms, and nonzero L contributions remain explicitly tested. Fixture runtime wall upper bound 0.551 seconds and small reference state sizes. No 8×4 q6 state vector is created.

The probe lemma holds because each probe colors its three matched pairs with three distinct colors, so only that matching survives. It applies to the Cartesian O(3) invariant delta-pairing span. It does not authorize interpreting spherical digits as Cartesian colors. Invariant operators composed from these Cartesian deltas preserve that span.

## Geometry, vacua, and sample scope

All 512 masks are unique, contain origin, and have exactly the specified colex rank floor(j·169910/511). Their internal-edge class histogram is independently verified as 55/131/176/111/28/9/1/1 for 0 through 7 edges. No zero-M or low-hit filter is present.

For each embedding B, the removed vacuum row is c times the projector onto empty B. Inclusion–exclusion gives c Σ_(T⊆B)(−1)^|T| product_(i∈T)n_i. The producer evaluates this polynomial by subset incidence; the second action keeps the original vacuum row on every embedding. Exact per-channel agreement validates the two treatments on all sampled supports, not only the producer's auxiliary geometry assertion.

Source caches remain bounded at 16,384 full support masks each. The independent comparison uses two bounded lazy caches, not a full q6 cache. A 512-target sample can access many neighboring source supports; it is still not a full origin-support sweep. The 32/6 occupied-site reduction is not applied to sample outputs or checksums.

## Cost gate and unexecuted proposals

The recorded N/F/L sample times scale to 2,716.661846390625 CPU seconds for 169,911 origin targets; this is approximately 45.28 CPU minutes for these three actions on analytic m alone. The tenfold empirical margin is approximately 27,166.62 seconds, before additional moment terms, generic chi/v work and setup. This fails the proposed 180-second gate. The dispersed sample is neither random nor a worst-case runtime certificate, and the result does not prove intrinsic infeasibility.

The proposed second 169911×15 int128 cache costs exactly 40,778,640 bytes; the fixed-source int64 variant costs 20,389,320 bytes. Their paper-fit memory totals are not measured peaks or permission to allocate a full cache or raise the budget.

The unexecuted Brauer proposal has correct elementary delta diagrams: pair creation/annihilation, hopping propagation, and triplet permutation minus contraction. Gluing compatible intermediate occupied legs gives paths with two external endpoints or closed loops, each loop contributing 3. The raw five-rung neutral key ceiling is independently checked as Σ C(5,q)^2(2q−1)!!=5,396; 193 blocks give 1,041,428 loose keys. The stated conservative coefficient envelope 12816·16·3^15 is below 2^42. This is an algebraically sound proposal subject to actual checked implementation, exact local-matrix comparisons and resource caps, not an accepted executable or performance claim. Overcomplete rank-high pairing keys must not be called a minimal basis. No Brauer computation was performed in this review.

## Resources, reproduction, and remaining limits

Single-core CPU7; runtime address-space cap 256 MiB; builds separately capped at 512 MiB. Main comparison was capped at 25 CPU seconds and completed at 13.7927; its actual usage is conservatively charged 14 seconds, freeing the unused reservation. Independent full local comparison was charged 2 seconds. Fixtures were charged 2 seconds. check.py was run once before fixtures existed and stopped on a missing-file error after the edge/stabilizer checks; it was rerun after fixture creation. Both checks are conservatively charged 3 seconds each. Including setup/metadata/tails, charge the complete review 30-second allowance; no numerical budget remains. An initial fixture compilation missed <set>; it was corrected before fixture execution, within the separate compilation cap. All numerical checks eventually completed; neither failed compilation nor premature checker result is treated as completed evidence.

To reproduce under a newly approved budget, copy the frozen review sources and source package to a fresh location, preserve their relative paths or adjust the explicit adapter include, and build independent.cpp, action.cpp (link -lgmpxx -lgmp), and cartesian_fixture.cpp with g++ -O2 -std=c++17. Do not run setup.py over the sealed review, because it records the initial scaffolding before the final probe test addition. Run independent REVIEW_DIR SOURCE_DIR; action SOURCE_DIR; cartesian_fixture REVIEW_DIR/fixtures; then check.py. Verify all source and review hashes first. Source REPRODUCE.sh is a producer replay and not a substitute for the independent comparisons.

No full 8×4 support contraction, full q6 cache/pass, global q8/q10 states, full 8×4 moments, new .11 endpoint, or new all-size gap follows. Any diagram compiler, new action sample, or expanded production resource gate requires separate authorization.
