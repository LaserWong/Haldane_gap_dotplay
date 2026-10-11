# Next local proposal, not executed

## Preferred route: O(3) invariant pairing diagrams

Request a separate local correctness-compiler gate of at most 60 CPU seconds, CPU6, one thread, 256 MiB address space, compilation separately at 512 MiB. This proposal itself grants no authority. Stop at a 55-second soft checkpoint or the 60-second hard CPU cap; report incomplete rather than increasing the limit. No full q6 cache, full 8×4 support pass or global q8/q10 states.

Reuse the verified Cartesian matrices as an exact reference. Represent a diagram by input/output occupation masks, an ordered pairing of occupied external color legs, and a signed integer coefficient:
- C†: the two outgoing occupied legs are paired by delta
- C: the two incoming occupied legs are paired by delta
- D hopping: pair the incoming triplet leg with its outgoing propagated leg
- D on two triplets: crossed propagation (permutation) minus separate incoming/outgoing singlet contractions

To compose, require equality of intermediate occupation masks, glue the intermediate color legs, and use union-find to trace paths. Each closed color component contributes exactly 3. Every open component must have two external ends, yielding a new pairing. Aggregate identical occupation/pairing keys exactly after every word and every support, including all signs and torus embedding multiplicities. Do not fit diagrams from a few matrix entries. The high-rank pairing representation can be overcomplete at O(3) dimension three; retaining an overcomplete exact representation is safe, but counting it as a minimal basis is not.

For a five-rung neutral local operator, the unconstrained raw key ceiling is Σ_(q=0)^5 C(5,q)^2(2q−1)!! = 5396 occupation/pairing diagrams. Across 193 N/F/L support blocks this gives a deliberately loose 1041428 keys before cancellations, above the planned 16 MiB record allowance at 32 bytes/key. Therefore enforce a hard live/serialized rule cap of 524288 32-byte-equivalent records including index overhead; exceeding it fails this representation gate. Streaming one support at a time prevents accumulation of reference matrices, but does not excuse a large final rule/index footprint.

The existing anchored signed-word counts are 536/9798/6446 after trace collection, with at most 32 initial occupation masks and at most 2^4 diagram branches per word. This gives a loose local branch ceiling about 8.59 million, not a runtime prediction. Before applying a compiled diagram to q6, join it with each of the 15 source matchings, keep spectator legs attached, count closed loops, and read the resulting output matching directly. This can remove the fifteen target-color probes and repeated matrix-unit/source-state traversals. Prove the spectator/matching mapping and compare every resulting local Cartesian matrix entry, including repeated edges and the fourfold support stabilizer.

Use signed int64 diagram coefficients with a proved composition bound, checked additions/products, and an explicit maximum intermediate loop count. A conservative proof may bound closed loops by the number of intermediate occupied sites, at most 15 for a length-four five-rung word; the resulting coefficient envelope 12816·16·3^15 is below 2^42. This bound is intentionally loose and must be checked against the precise composition representation. Global source/action contraction still uses checked int128 plus exact GMP import as warranted by source bounds.

Deliver surviving diagrams, occupancy classes, index memory, maximum coefficient/loop counts, exact comparisons against all saved Cartesian reference matrices, and both physical fixtures with all 15 terms. Only after independent acceptance propose a separately budgeted action sample against the present matrix-unit implementation on the same 512 targets. No production timing is implied by a successful compiler.

## Would a second analytic-m cache rescue the matrix-unit route?

The sample already has a 99.105% lazy-m cache hit rate. Cold/warm lookup batches cost 1.111/0.332 microseconds per call, including unranking and loop overhead. Multiplying the observed miss count by this difference gives approximately 0.207 sample seconds, versus 8.186 total sample seconds. This diagnostic suggests that eliminating analytic-m misses alone is a small improvement; it is not a rigorous speedup bound. A dense array could also change hit costs, but an origin-normalized array adds translation, sorting and channel-permutation work. That tradeoff has not been measured.

A second 169911×15 int128 cache costs 40778640 bytes. For this fixed m only, the proven <2^33 channel bound permits int64, costing 20389320 bytes. Added to the previous full-moment design total 87289472 bytes, the nominal totals are 128068112 or 107678792 bytes. Both exceed 100 MiB; both fit 128 MiB on paper (roughly 5.86 MiB or 25.31 MiB spare, respectively), and 192 MiB gives more room. These are design sums, not measured production peaks, and the new index sizes/runtime must be included without double-counting the old reserve. No budget expansion to 128/192 MiB is authorized here.

A full unnormalized 906192-support int64 m cache would alone cost 108743040 bytes; it is a different and substantially larger design. Do not silently substitute it for the origin-normalized cache or assume translation invariance removes permutation cost.

A larger CPU budget is possible only by a new root decision. The current approximately 45.3 CPU minute mean projection covers N/F/L on m only, with no safety factor and no chi/v or remaining moment work. A credible whole-moment proposal must price all these costs, setup/cache fill, arithmetic widths, checkpoints, and independent review before asking to expand the existing 180-second gate.
