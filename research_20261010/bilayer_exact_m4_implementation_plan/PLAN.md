# Implementation plan for exact 8×4 Krylov moments

Planning only, 2026-10-11 00:26 UTC / 2026-10-10 20:26 EDT. No new physical run, motif generation, compilation, support sample or full contraction was executed to prepare this document. Counts are combinatorial upper bounds. No production permission is implied.

## Decision

A single-vector implementation can fit a 100 MiB address-space budget, but the connected-commutator contraction time is not yet known to be feasible. Implement and independently validate compact signed local operator rules first. Do not start a full 8×4 support pass, and do not spend a pass on m3 alone. The accepted generic-m4 envelope barrier already excludes the selected .11 targets of this fixed vector.

The smallest useful next deliverable is a streamed local-rule compiler for Nop=[C,[D,C†]], F=[E†,E], L=[[C,K],C†], plus a generic scalar q6 lookup. It must report cancellation counts, surviving rules, transition counts and actual lookup cost. A naive per-support scan of all raw motifs is rejected quantitatively below. This plan does not promise that motif cancellation will be sufficient.

## Frozen mathematical inputs

Model: ordinary periodic spin-1/2 bilayer H′=Q+(g/2)(C+C†+D). N=32 rungs, 8×4 graph, 64 unit-weight rung edges, 128 physical intralayer bonds. Full Hilbert dimension 4^32=2^64. Use the exact 57-dimensional .11 witness in bilayer_split_pencil_optimization/result.json, with independent endpoint and complete-matrix acceptance retained. Read coefficients in order B15,L14,R14,M14. Do not identify cR with cM. ψ has q≤6 and m=ψ6=M cM. The desired new search space is only {ψ,H′ψ}. Scalar moments do not supply a complete 58-dimensional augmentation.

Use integer T=dQ+hA with d=200,h=11. Obtain m0,m1,m2 from the accepted full matrices and compute integer m3,m4, then divide by ||ψ||² d^k. Check new low-order results against accepted inputs before using either new moment. The small physical fixtures have independent acceptance, including all 15 individual signed terms and nonzero 5×2 q10. They evaluate commutators by sparse composition and do not provide a production local-rule implementation.

## One large cache rather than two

For any sector support S, store coefficients in its invariant pair-matching basis, not explicit Cartesian color states. q2/q4/q6 have 1/3/15 matching channels. The q6 Gram has entries 3^(number of loops in the union of two matchings). Preserve oriented bilinear products. Matching Gram matrices do not make a nonsymmetric operator symmetric.

1. Build scalar ψ4=L cL+R cR and χ4=(Tψ)4 on all 35960 q4 supports. These two int128 caches cost 2×1726080=3452160 bytes. The existing 14-column int32 R cache costs 6041280 bytes. Retain it only during source preparation if needed.
2. Define m(S) analytically using the existing Mval formula contracted with cM. Do not allocate a second q6 cache for m, Dm or Km.
3. Build χ6=6d m+h(C†ψ4+Dm) once on all 169911 q6 supports containing the origin: 169911×15×16=40778640 bytes. An arbitrary q6 support is translated to put one occupied rung at (0,0), sorted and its matching labels permuted into the stored order.
4. The high-sector auxiliary vector satisfies the exact identity
   v=8dh m+hχ6+h²Dm=2dh m+2hχ6−h²C†ψ4.
   Thus generic v lookup needs χ6 lookup, analytic m and at most 15 occupied-edge removals followed by ψ4 lookup. There is no v cache and no division by h.
5. CM and E†m live on q4. Optional full int128 caches for both add 3452160 bytes. They can also be streamed if memory is tighter. γ=C†Cm+Km is produced one target support at a time. Lower q0/q2 scalar images are negligible.

Peak planned payload with old R retained, two q4 source caches, two q4 auxiliary caches, one q6 cache, and 720×15 one-byte matching permutations is 53735040 bytes. Reserve at most 16 MiB for compact motif rules/indexes and 16 MiB for allocator/runtime/GMP/buffers: total 87289472 bytes, below 104857600 by 17568128 bytes. This is a design budget, not measured RSS or proof about a particular allocator. Impose RLIMIT_AS as well as record RSS. Release R after source construction when possible. A dense hash map with one entry per physical q6 Cartesian state is forbidden.

## Generic lookup and translation proof obligations

Use torus translations (x,y)→(x−x0 mod 8,y−y0 mod 4), not integer-index cyclic shifts. Mval depends on translation-invariant edge weights and pair-orbit labels. L,R and the source coefficients must have the same property. D,C,C† commute with all translations, so ψ,χ6 and v inherit invariance. For an arbitrary sorted S, any of its six occupied sites may be translated to the origin. The six answers must coincide after the corresponding permutation of all 15 matching channels. This is a proof requirement and a fixture test, not a floating tolerance. Precompute all 720 permutations and their induced matching maps.

For a translation-invariant scalar density f(S), summing over supports with origin occupied and multiplying by N/q gives the complete sum, even for periodic supports with stabilizers: double count the pairs (S,occupied site). Use exact rational weighting or verify divisibility after summation. q0 is separate. The local fixture's localized ψ is not translation invariant and cannot itself justify the reduction. Use translation-symmetrized small fixtures for that test.

Ordered edge-tuple translation reduction is a different organization of the same sum. On 8×4, a nearest-neighbor undirected edge has no nontrivial translational stabilizer, so an ordered tuple has 32 translates. Its first edge can be anchored to one of two positive directions. This permits storing motif templates divided by 32, but applying them to a fixed-origin target support still needs all relevant translated embeddings. Never divide both the support count and the embedding count by 32. Motif-first contraction instead retains the full spectator support sum and counts orbit stabilizers explicitly.

## Signed connected local-rule compiler

The local letters c_e,c†_e,d_e act on two rungs. Operators with disjoint supports commute, so enumerate nested connected tuples only, preserving each order and multiplicity. Repeated edges are allowed. For E=[D,C†], enumerate touching ordered edge pairs. For Nop=[C,E], the added edge must meet the pair's union. For L=[[C,K],C†], use connected-prefix quadruples. For F=[E†,E], each pair is internally connected and the two unions meet. Either edge of the second pair may first touch the first pair. Use the corrected conservative ceiling 172032, not 86016, for F.

Canonicalization must include the actual torus embedding and an explicit permutation back to local rung labels. Do not silently identify graph-isomorphic motifs whose embeddings/multiplicities differ. Translation canonicalization is safe only with the preceding proof. Point-group identification is optional and requires another symmetry proof. It is unnecessary for the first implementation.

Expand each commutator into signed words before combining coefficients. Nop has four three-letter words. F and L each have eight four-letter words. Compile one local support at a time (at most five rungs, local Hilbert dimension≤1024). Accumulate identical transitions with signed integers and delete exact zeros. Do not allocate a dense local matrix per embedding. Dense 1024² int64 storage for even 5376 templates exceeds 42 GiB.

Production representation should be occupation projectors plus invariant contraction/permutation diagrams on the triplet indices. Composition joins diagram legs. Every closed color loop contributes 3. Occupation projectors implement the hard-core constraint at every intermediate letter. External spectator pairings must remain attached while diagrams reconnect local legs. Compile to target-occupancy-mask-indexed pull rules mapping a source support and its pair matchings to the target channels. This supports a generic q6 scalar lookup without a physical q8/q10 state. Internal local words may temporarily occupy additional local rungs. Those are ≤5-rung symbolic indices, not global support enumeration.

Compare each resulting diagram against all Cartesian local matrix entries for every surviving canonical motif, including repeated-edge cases, rather than fitting from a few states. Test Nop orientation as written. F and L must be Hermitian, while Nop need not be. Separately verify E†=[C,D]. Retain the negative −<Cm,K Cm> term. Extract local vacuum diagonal rules and sum their geometric multiplicities analytically. Otherwise even empty motifs cause huge unnecessary loops. Index nonvacuum rules by occupied target sites, deduplicate embeddings, and inspect local occupancy masks before requesting source amplitudes. Exact cancellation and occupancy pruning are essential, not optional optimizations.

## Scalar contraction schedule

- q≤6: χ is known. zq=dqχq+hDχq+hC†χ(q−2)+hCχ(q+2), except z6 replaces the q8 pull by h²γ. Accumulate ||zq||² exactly. z6 needs generic Dχ6 but not a second cached image.
- m3 high sector: use the accepted D8 identity, γ and oriented q6↔q8 coupling. Reuse Nop m from the m4 work. Do not launch a separate full pass for m3.
- q8: compute ||Cv||²+<v,Kv>+2h²<v,E Cm>+2h²<v,Nop m>+h⁴(||E†m||²+<m,Fm>).
- q10: compute h⁴[||γ||²+2<Cm,C Km>−<Cm,K Cm>+||Km||²+<m,Lm>]. For <Cm,C Km>, use adjoint contraction <C†Cm,Km> on q6. This avoids a second generic q6 image cache or nested q4→q6→q6 lookup.
- Likewise <v,E Cm>=<E†v,Cm> may be contracted on q4 if cheaper, but benchmark it against direct local raising rules before choosing. Keep its value separate from <v,Nop m>.
- The left vector m is identically zero on some supports, allowing skips in <m,Fm> and <m,Lm> only. No M-active filter is valid for ||Km||², ||z6||², <v,Kv> or the Nop cross. Existing source-family zero supports must stay included.

Accumulate all norms and bilinears in GMP integers. Existing scalar code narrows int128 to long in inner(). That routine cannot be reused for the larger coefficients. Import signed int128 exactly into mpz, or use a proved checked smaller representation. Establish an explicit absolute coefficient bound for this frozen witness, every source image and compiled rule. If any amplitude cannot fit int128, redesign and recost before execution. Checked additions and products are required, but checks alone do not bound runtime or memory.

## Operation ceilings and present barrier

q4 has 4495 origin-containing supports (35960 full). q6 has 169911 (906192 full). A direct q6 D pull uses at most 24 external-neighbor lookups plus 15 occupied-pair terms per support. Generic K uses at most 72 ordered-wedge lookups,15 occupied-edge tests and 64 vacuum-edge tests per support. The existing M-specific implementation is not sufficient. A Cv q4 pull scans at most 64 empty edges per support. Count each 15-channel contraction and its GMP products separately.

The raw counts satisfy connected triples≤5376, connected-prefix quartets≤86016, and F quartets≤172032. The q6 Cartesian product with the latter is 29230129152 raw tuple/support visits for F alone. Eight four-letter words can each branch up to 3^4=81 times in a Cartesian local action: a deliberately loose bound is 18941123690496 leaf visits before source-matching contraction. Nop and L add further work. These are not runtime estimates. They demonstrate why raw enumeration is unacceptable. Existing ~3.5-second scalar residual timing does not estimate nested-motif performance.

Templates anchored under translations have ceilings 168/2688/5376, but this is only a storage/compiler reduction. There is no established upper bound on surviving compressed rules small enough to guarantee useful runtime. The 16 MiB rule budget corresponds to at most 524288 records if the serialized record is 32 bytes, less after index storage. Exhausting that budget is a hard gate failure, not permission to grow it.

## Proposed gated work, requiring fresh approval

A. Local compiler and symmetry validation: compile separately under 512 MiB. Run under CPU 3,5 CPU seconds,100 MiB, checkpointing templates and counters. Stop at the cap and report incomplete counts. This is local operator algebra, not a full 8×4 support pass. Require exact agreement with all ≤5-rung local matrices, translation/matching invariance on symmetrized 4×2/5×2 fixtures, and all independently accepted 15 term checks. A larger local validation budget needs explicit approval.

B. Small sampled production-action benchmark: after A is accepted, propose another ≤5 CPU seconds/100 MiB on CPU 3. Build only necessary sampled scalar cache entries using an independently checked analytic χ6 fallback. Do not silently build the full 169911 cache. Sample deterministically across occupied-edge counts, source-zero/nonzero supports, distant supports and wraparound motifs. Include worst observed transition classes. Report cache-hit and cache-miss lookup costs, actual rule visits, GMP limb sizes, setup costs and extrapolation by exact class counts. Samples cannot prove a universal performance upper bound, so retain a safety factor and separate the measured estimate from the hard cap.

C. Only if correctness passes, memory payload is verified below 100 MiB and a conservative 10× empirical extrapolation plus all setup/cache-build costs fits 180 CPU seconds, submit a one-pass production proposal with that hard budget, checkpoints and exact abort behavior. The 180-second threshold is a proposed decision gate, not current authority or a mathematical runtime guarantee. If reduction remains too weak or projection is inconclusive, report the exact dominant rule family and stop. Do not replace the blocked route with q8/q10 enumeration.

A full authorized run, if later feasible, must preserve each separate contribution, match m0/m1/m2 exactly, assemble the 2×2 complete moment pencils and undergo independent physical review. Only then test the specified .11 lower endpoints with the full even-sector cutoff and global-ground identification. Neither moment agreement nor a two-vector Ritz energy alone is an all-size gap certificate.
