# Complete third- and fourth-moment calculation plan

Design only, 2026-10-11 02:40 UTC / 2026-10-10 22:40 EDT. Prepared after freezing the Brauer compiler. No new compilation, physical computation, support sample, cache build or production action was performed for this proposal. Every new runtime budget below requires a root decision. A possible one-to-three-CPU-hour allocation is not existing authority.

## Proposed calculation

A useful cost estimate requires a complete scalar-moment implementation, validated on small systems and then sampled as a whole. The Brauer representation eliminates redundant color calculations, but the current 764.181-second projection measures only N/F/L actions on m. It omits most of the moment calculation and cannot decide whether a one-to-three-hour run is feasible.

The next requested gate is a separately authorized maximum 300 CPU seconds / 256 MiB, CPU6 single-threaded, with compilation separately capped at 512 MiB. It covers missing operator/source integration, complete small physical fixtures, and bounded whole-pipeline targets. Soft-stop at 270 CPU seconds, retaining completed blocks. No automatic restart or larger budget. No full 8×4 q4/q6 support sweep/cache is included in that gate. Root may choose a smaller staged budget instead.

Only after producer and independent review pass should root choose a full-job memory/CPU allocation. Suggested options to evaluate are 3600 or 10800 total CPU seconds, with whole-process-tree accounting and an independently budgeted review. These are proposals, not launch instructions.

## Frozen physical task

The ordinary periodic spin-half bilayer on 8×4 rungs has 32 unit-weight rung edges and 64 edges in the rung-plane graph, with full Hilbert dimension 4^32=2^64. The archived source incorrectly states that there are 64 rung edges. This reader edition corrects that counting typo. H′=Q+(g/2)(C+C†+D), g=11/100. Integer T=200Q+11(C+C†+D), d=200,h=11. Use the accepted integer 57D witness in coefficient order B15,L14,R14,M14. Preserve cR separately from cM.

Let ψ be the full q≤6 witness, m=ψ6=M cM, χ=Tψ, z=Tχ, K=[C,C†], E=[D,C†], E†=[C,D], N=[C,E], F=[E†,E], L=[[C,K],C†]. Desired scalar outputs are <ψ,ψ>, <ψ,Tψ>, <χ,χ>, <χ,Tχ>, <z,z>, each as an exact integer with its unnormalized convention. Normalized physical moments divide by ||ψ||²·200^k.

The resulting moment pencils describe only span{ψ,H′ψ}. They do not provide the complete 58D augmentation, a new endpoint, or a gap certificate without the separate pencil/sector/global-ground review.

## Cache/source construction and dependencies

Use the accepted generic q6 translation/matching lookup, replacing only its scalar source builder as explicitly checked below. No Cartesian-color state cache and no global q8/q10 support enumeration.

1. Read and hash-bind the witness, geometry/orbit labels, accepted m0/m1/m2, rule manifests, and full-matrix review. Check coefficient ordering and all 57 coefficients before allocating large storage.
2. Build ψ0 and the full 496-entry scalar ψ2. Build scalar ψ4=L cL+R cR on all 35960 q4 supports in an eventual full job. An existing R14 cache is 6041280 bytes. Use it only for construction if useful, then release it. A bounded pilot uses lazy R/q4 entries instead and must price the difference.
3. Optionally build scalar m on the 169911 origin-containing q6 supports. For this fixed witness each matching channel fits int64 (<2^33). Storing it uses 20389320 bytes. Analytic m remains the default correctness fallback. This optional cache is a setup/memory decision, not a silent second full cache.
4. Build full scalar q4 caches cm=Cm and ed=E†m. Prefer direct connected E† diagrams for ed rather than repeatedly forming C Dm−D Cm through generic nested lookups. Add E/E† diagrams (14 anchored touching ordered pairs, 28 signed words each) and validate their q6↔q4 matching action. Generic K4 on cm uses the already verified neutral commutator kernel or an independently validated diagram equivalent.
5. Compute χ0, χ2 and χ4 from Tψ, including every neighboring sector. In particular χ4=800ψ4+11Dψ4+11C†ψ2+11cm. Store full scalar χ4. Do not retain Dψ4 or χ images unnecessarily.
6. Build the one int128 χ6 cache on all 169911 origin supports, using χ6=1200m+11(C†ψ4+Dm). Generic source queries translate an occupied site to the origin, sort, and permute all fifteen matching channels. Verify every permitted anchor on small fixtures. The cache build itself must be measured and counted, not hidden inside a cheap hit estimate.
7. Supply v generically from v=2dh m+2hχ6−h²C†ψ4. Cross-check against v=8dh m+hχ6+h²Dm on fixtures and samples. This uses one χ6 lookup, analytic/cached m, and occupied-edge q4 removals. There is no second v cache. The C†ψ4 pull has at most fifteen occupied-pair tests and only actual edges contribute.

The first implementation should use deterministic complete cache fills and simple full q4 addressing. Translation-orbit fills can later avoid repeated equivalent builder work, but require an explicit ready/coverage proof and stabilizer tests. Do not assume a factor-of-six cache-build speedup merely because the final source is translation invariant.

## Joint contraction schedule

Use complete q0 and all 496 q2 supports. Use 4495 origin-containing q4 and 169911 origin-containing q6 supports for final scalar densities, with exact weights 8 and 16/3 respectively. Cache construction and contraction enumeration are different operations. q6 translated operator embeddings are never divided by 32 a second time. For each named q6 scalar contribution verify the exact division by three at final normalization, or retain an exact rational until cancellation is justified.

### Low sectors and low-order controls

For q=0,2,4,6 form zq=dqχq+hDχq+hC†χ(q−2)+hCχ(q+2). At q6 replace the q8 pull with h²γ, where x=C†cm and γ=x+Km. Add ||zq||² separately for each q. Streaming z6 requires a generic Dχ6 action and no second q6 image cache.

Recompute m0,m1,m2 from the source/cache pipeline and require exact agreement with the accepted complete matrices before reporting m3/m4. m2 uses ||χ≤6||²+h² n8, where n8=||cm||²+<m,Km>. This checks the q8 source norm without building q8 states. Check all low-sector χ images and norms separately on physical fixtures.

For m3 add the q≤6 diagonal terms dΣq q||χq||²+hΣq<χq,Dχq>, the adjacent low-sector cross terms 2hΣ(q=2,4,6)<χ(q−2),Cχq>, and the high-sector terms 8dh²n8+h³d8+2h²<χ6,γ>. Preserve the exact orientation of d8 below.

### All fifteen named signed terms

Keep these as individually labeled GMP accumulators, matching the previously accepted fixture names and scaling.

| # | Named term | Evaluation sector/source |
|---|---|---|
| 1 | D8_2_CM_CDM = 2<cm,C Dm> | Use adjoint identity 2<x,Dm> on q6, retaining the original label |
| 2 | D8_minus_CM_DCM = −<cm,Dcm> | q4 cm cache and D4 action |
| 3 | D8_KM_DM = <Km,Dm> | q6 analytic/cached m images |
| 4 | D8_nested_C_E = <m,Nm> | q6 N diagram action |
| 5 | Q8_Cv_norm = ||Cv||² | q4 pull of generic v |
| 6 | Q8_v_Kv = <v,Kv> | q6 generic K action with v lookup |
| 7 | Q8_cross_ECM = 2h²<v,Ecm> | q6 E diagrams acting on q4 cm cache |
| 8 | Q8_cross_CE = 2h²<v,Nm> | Reuse the same Nm image. The left vector is v |
| 9 | Q8_EadjM_norm = h⁴||ed||² | q4 ed cache |
| 10 | Q8_Ecomm = h⁴<m,Fm> | q6 Brauer F action |
| 11 | Q10_gamma_norm = ||γ||² | q6 γ=x+Km |
| 12 | Q10_2_CM_CKM = 2<cm,C Km> | Use 2<x,Km> on q6, no C Km cache |
| 13 | Q10_minus_CM_KCM = −<cm,Kcm> | q4 generic K4 on cm cache. The negative sign is mandatory |
| 14 | Q10_KM_norm = ||Km||² | q6 reusable Km image |
| 15 | Q10_L = <m,Lm> | q6 Brauer L action |

Then d8 is terms 1–4. The q8 z-norm is terms 5–10. The q10 z-norm is h⁴ times terms 11–15. Add all four low-sector z norms for m4. Do not absorb the negative K4 contribution into an undocumented combined term. Do not symmetrize N or replace an oriented cross term by a different matrix element.

### Reuse within each pass

A joint q6 target step should compute m,χ6,v,Dm,Km,x,γ,Dχ6,Nm,Kv,Ecm and the needed Fm/Lm, then accumulate all relevant norms/cross products and z6. These are small temporary fifteen-channel arrays, not full source-image caches. Nm serves both D8 and the v cross. Km/x serve every q10 expression. Fm and Lm may be skipped only when their left m vector is identically zero. Retain counters and tests for that optimization. No M-active filter is valid for z6, Kv, Nm's v cross, ||Km||², or other images with different left vectors.

The joint q4 step should share the empty-edge source pulls for Cχ6 and Cv when practical, using one χ6 fetch and the v formula on the same source. It also handles Dχ4, Dcm, Kcm, ||cm||² and ||ed||². cm/ed are already cached. A straightforward Cv pull has at most 64 edge candidates per target. Generic D6 has at most 24 neighbor-source moves plus 15 occupied-pair terms, and generic K6 at most 72 wedge-source candidates plus occupied/vacuum terms. Actual weighted/source requests must be instrumented.

## Candidate memory allocations

An explicit production memory decision is still required. The following is a revised design using compact Brauer indexes. These estimates revise the predecessor's 87 MB design and do not represent measured RSS.

| Item | Bytes |
|---|---:|
| One χ6 int128 cache, 169911×15 | 40778640 |
| Four full scalar q4 int128 caches: ψ4,χ4,cm,ed | 6904320 |
| Brauer/E/E†/generic operator and incidence index allowance | 8388608 |
| q6 matching permutation table | 10800 |
| q0/q2 vectors and small tables allowance | 65536 |
| Checkpoint/I/O working buffers | 2097152 |
| Allocator/runtime/GMP allowance | 16777216 |
| Design total without optional m cache | 75022272 |
| With int64 m cache | 95411592 |
| With int128 m cache instead | 115800912 |

Release the 6041280-byte R14 cache before the χ6/m phase. Actual peak must include temporary builder/index allocations and all children. On these assumptions the int64-m design is below 100 MiB, but its margin is not permission to run. A limit of 128 MiB provides a safer explicit candidate cap. The int128-m version fits 128 MiB only on this revised budget. A 192 MiB option can be considered only if measured needs justify it. No full unnormalized 906192-support m cache is proposed.

The previous matrix-unit sample already achieved a 99.105% lazy m hit rate, so a second m cache should be chosen from a measured whole-pipeline benefit, not assumed to rescue runtime. The Brauer kernel fetches all channels together and substantially reduces source requests. Dense origin lookup also requires translation, sorting, and permutation. Compare it against analytic and capped-lazy alternatives on the same whole-pipeline sample.

## Integer safety and GMP requirements

A deliberately broad source bound can be derived before implementation. All frozen witness coefficients have magnitude at most 2^48. A q2 orbit-vector combination has l1 norm below 496·3·2^48<2^59. Each of C,C†,D has full-column l1 norm at most 192<2^8 on this graph. L=C†B, R=DL and M=C†L then give ||ψ||1<2^77 after summing all four source families and the vacuum. Also ||T||1≤200·32+11·3·192<2^14. Therefore each T²ψ amplitude is below 2^105, and the displayed nested source images admit bounds below signed int128 using at most four elementary factors and their explicit scalar d/h prefactors. The implementation must enumerate every cached/intermediate source in a bound table. Do not silently infer that every possible future expression is covered.

For the optional m cache the sharper exact formula gives each matching coefficient ≤6 max|cM|<2^33, validating int64 storage. Generic invariant coefficients can be bounded by their exact Cartesian probe amplitudes. Use checked int128 adds/products in construction and source actions. Never reuse the old inner() path that narrows through long. Import signed int128 to GMP through its two uint64 words and sign, already exercised in the Cartesian sample. Norms/bilinears, term scaling, normalization and moment assembly are GMP integers/rationals.

Import each fifteen-channel temporary vector once per target and reuse its GMP values across bilinears. Record actual imported/product/accumulator limb sizes, nonzero Gram products, conversion counts and GMP CPU time. Dense χ/v vectors may cost much more than sparse m-source products. The m-only sample cannot price them.

## Required physical checks

Complete the following checks before any 8×4 whole-moment sample.

1. Validate new E/E† rules against every local Cartesian entry, including repeated edges, weights, adjoints, source/target occupation changes and stabilizers. Check general qi=4→qo=6 and qi=6→qo=4 diagram contractions with spectator pairings.
2. Replay the localized 4×2 and 5×2 fixtures in full support mode and compare every cached source, χ/z sector image, all fifteen terms, m0 through m4, and the nonzero 5×2 q10 term against direct physical T²ψ. No translation reduction is allowed for these localized vectors.
3. Add translation-symmetrized versions and a generic nonzero B/L/R/M small witness. Verify every q6 occupied-anchor choice, matching permutation maps, both v formulas, exact N/q normalization, and source-zero targets with nonzero χ/v images. Compare the reduced and full scalar computations exactly, including supports with stabilizers.
4. Deliberately test orientation/sign mutations. The changes N→N†, deleting Q10's negative K4 term, conflating cR/cM, omitting a q8 cross, and applying an M-active filter to Kv/z6 must fail a relevant fixture.
5. Validate serialization, round-trip restart and no-double-count accumulation on the small fixture before production design acceptance.

A producer test pass is not independent review. Give the reviewer the complete sources, bound table, all outputs and sealed input identities.

## Bounded whole-pipeline sample and cost accounting

After the local/physical checks pass within the proposed gate, sample no more than the same 512 q6 targets, no more than 128 dispersed q4 targets, and optionally all q≤2 targets. Lazy source working sets may contain neighboring supports but must have explicit caps (e.g. at most 50000 χ6 entries and separately capped q4 entries). This is not permission to fill the full q6 or q4 caches. If capped misses contaminate warm timings, report it rather than extrapolating a warm-cache claim.

Record the following quantities by target source-zero/edge/wrap/stabilizer class.
- ψ4,cm,ed,χ4 and χ6 builder costs, calls and channel writes
- analytic m versus cached m, χ6 hit/miss and v reconstruction costs
- Dχ6, Km, Kv, Nm, Fm, Lm, Ecm and q4 Cχ6/Cv work separately
- diagram/matching/embedding hits and actual source requests, with no scalar-color scans
- each named term's GMP product/import/limb costs and all low-sector norm costs
- resident/address-space peaks, cache fill/eviction counts, disk checkpoint bytes and CPU
- production-valid left-m skipping only for F/L, alongside a no-skip correctness comparison

The pilot must execute the full target-step dataflow and accumulate every named term, not just time disconnected operator calls. Cross-check sampled channels against independent/direct small fixtures and permitted reference actions. Partial sampled scalars are not physical full moments.

Use the explicit cost model below.

T_total = T_input/rule setup + T_ψ4/full + T_cm/full + T_ed/full + T_χ4/full + T_χ6/full + optional T_m/full + 169911·t_joint_q6 + 4495·t_joint_q4 + T_q≤2 + T_checkpoint/finalization.

Cache construction costs use their actual full cache sizes (35960 q4 entries and 169911 q6 entries), even though contraction counts are smaller. If an orbit-fill optimization is implemented, replace those builder counts only after its coverage/multiplicity proof passes. Add expected cache-hit paths only after the corresponding source has been fully built in the proposed production schedule.

The historical generic q6 fixture had 8469 cache fills/12023 lookups and .117699 seconds for 129 q6 targets. Its approximately 158-second full-pass estimate was for a different 58D residual task. It is useful as a sanity check only. The present Brauer 764-second projection is for N/F/L on m and omits dense χ/v/GMP and the valid F/L left-m skip. Neither number substitutes for this whole-pipeline sample.

Retain the existing tenfold empirical factor as the conservative default unless root explicitly approves a different factor after seeing measured class coverage and discrepancies. Full-job approval requires the selected complete cost model, setup and finalization reserve to fit the chosen cap. If the estimate does not fit 3600/10800 seconds, return the dominant costs and an optimization proposal. Do not launch or declare intrinsic impossibility.

## Full-job checkpoint/termination contract, still unapproved

A proposed full run should be one single-threaded process tree with one state directory and a monotone no-refund CPU ledger. Reserve each batch's CPU allowance before starting it. Charge failed/terminated batches, never reset the ledger on retry. Use the previously reviewed corrected launcher/outer-accounting design rather than reintroducing an orphan-child path.

Cache phases have a coverage bitmap, deterministic entry IDs, hashes and completed ranges. Contraction batches cover disjoint deterministic q0/q2/q4/q6 ranges and save all individual GMP term accumulators. Write a completed batch atomically only after all its named contributions finish. An interrupted partial batch contributes no scalar totals. Recalculation is charged and requires remaining authority. Resume from the same sealed inputs and checkpoint, not a second concurrent job.

Stop admitting work before the research deadline 2026-10-14 00:00 UTC, leaving an explicit finalization reserve. At a CPU/memory/deadline stop, report incomplete coverage and exact spent/remaining budget. No partial sum is a completed moment or certificate.

After exact m0/m1/m2 consistency, full coverage, all signed terms and normalization pass, freeze producer m3/m4. Independently verify the implementation and full outputs before assembling/using the 2×2 moment pencils for the requested .11 endpoints. An independent replay may need its own one-to-three-hour-scale allowance. It is not free or implicitly covered by the producer cap.

## Proposed calculations requested from root

1. Approve or revise the next 300-CPU-second bounded whole-pipeline implementation/fixture/sample test without a production run.
2. After measured results and independent review, choose a full-job cap (potentially 3600/10800 seconds) and memory cap (100/128/192 MiB), with a separate review budget.
3. Approve any departure from the default tenfold safety factor only with the complete measured cost breakdown.
