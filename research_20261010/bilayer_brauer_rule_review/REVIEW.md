# Independent Brauer local-rule and sample review

2026-10-11 02:40 UTC / 2026-10-10 22:40 EDT.

**PASS for the local Brauer compiler, small fixtures and specified 512-target sample. The 180-second production-cost gate still fails.** No fundamental infeasibility or new gap claim.

Source package: `../bilayer_brauer_rule_compiler`, manifest `7eeb2e2c2adbfe000471c64e464fbf2b74becbd218ec4e1b4e7245472f72f6ec`. All source entries, pinned inputs and predecessor seals verified unchanged. In particular the Cartesian source seal `760ab0e980cc40bd96028da1bc626353c44f463148d5dd2bc6cef81db566d1bd` and its independent review seal `8778764242be53f587f68b7416d7cf114cb0182b505089fbd85a7ffe224c1979` remain intact.

## Composition and physical conventions

The stored external legs are incoming 0..4 and outgoing 5..9, with inactive nibble 15. Independent expansion validates occupation-neutral masks, the active/inactive leg condition, symmetric partner involution, no self-pairs and no unused high key bits.

C creates no outgoing triplets and contracts its two incoming triplets; C† creates a delta pair; D hopping propagates the occupied color; on two triplets D is permutation minus incoming/outgoing contraction. Spectator identities are explicit. These agree with the independently accepted Cartesian physical edge operator and ordinary bilayer normalization H′=Q+(g/2)(C+C†+D). The oriented N=[C,[D,C†]], F=[[C,D],[D,C†]], L=[[C,[C,C†]],C†] word construction remains unchanged from the accepted connected compiler.

Composition requires outgoing occupation of the first diagram to equal incoming occupation of the second. Its layered graph has degree-two interior color vertices and degree-one external vertices. Thus each connected component is a path with two external ends or a closed component with no external ends. A closed color component gives exactly three summed colors; it must not be counted as one, a sign, or an extra external pairing. All-vacuum composition has no active component and factor one.

The review checks the producer union-find result against an independent adjacency-list depth-first traversal for 58,000 composition cases. The suite includes all 32 initial masks, every elementary operator on all ten five-site pairs, and every distinct diagram reachable through three elementary stages. It verifies both resulting pairing key and loop factor. Final length-four commutators are independently checked through complete Cartesian matrix expansion below. Incompatible occupations are rejected by the explicit composition assertion.

## Exact local diagrams and stabilizers

The compiler is rerun into the review directory and all three diagram files are byte-identical to the source seal. Separately, review code reads saved 20-byte records, assigns colors to external pairs, and expands them without using the producer expand_diagrams routine. Every nonzero entry and omitted zero agrees with the independently accepted Cartesian reference matrices:

- N: 634 diagrams, 27 support blocks
- F: 14,532 diagrams, 83 support blocks
- L: 1,941 diagrams, 83 support blocks

Total 17,107 diagrams and 342,140 serialized bytes; 121,251,328 implicit local matrix entries are covered. A high-rank pairing representation may be overcomplete; correctness comes from equality of the represented matrices, not a minimal-basis assertion.

The regenerated compiler checks the order-four support stabilizer occurring once per family, with all other stabilizers trivial. Exact equality to the already independently checked Cartesian matrices transfers their stabilized F/L Hermiticity. The action comparison below retains all 32 embeddings including equal support masks with different site permutations. No additional support-stabilizer division, point-group quotient, or 1/32 occurs.

## Full small fixtures

Both 4×2 and 5×2 full unquotiented Brauer compilations were rerun. Their six complete N m/F m/L m vectors equal direct nested physical Cartesian vectors exactly, including doubled vertical edge weights. Fifteen-probe reconstruction of these outputs passes. This rerun uses the producer small-graph harness; its direct physical edge and probe convention were independently accepted in the predecessor review and rechecked at startup.

All regenerated fixture and term JSON are exactly equal to the frozen source outputs, including all fifteen signed terms, m3/m4, sector norms, negative and oriented contributions, nonzero 5×2 q10 and cancelled 4×2 q10. There is no 8×4 global q8/q10 reference vector.

## Independent 512-target action

The Brauer action is compared directly against the independent all-embedding Cartesian implementation from the accepted previous review, rather than only the producer's indexed color reference. This second implementation scans every translated Cartesian block, preserves spectator colors, retains vacuum rows explicitly, and evaluates analytic source coefficients through its separate formula/cache. It does not call Brauer composition, Brauer source-to-output graph contraction, occupied-site incidence selection or the vacuum inclusion–exclusion evaluator.

Every one of the 23,040 output channels agrees exactly: 3 families × 512 targets × 15 channels. All 512 dispersed colex targets are included in every family, including 285 with identically zero input source and 227 nonzero. Diagram-hit totals equal the source report: N 264,312; F 1,717,692; L 683,326. Source geometry and fourteen cM coefficients are byte-identical to the accepted Cartesian input. Matching order is a shared convention; the reference source amplitude implementation is separate and explicitly compared against analytic channels.

This validates occupancy selection, source support construction, spectator wiring, loop weights, output matching identification, signs, all ordered translations and vacuum contributions on the stated sample. Because the reference retains original vacuum rows, agreement independently exercises the producer's separated vacuum-projector inclusion–exclusion path. A 512-target check remains a bounded sample, not a complete q6 support sweep.

## Resource and cost conclusions

The combined review executable took 12.7186 CPU seconds and peak RSS 43,604 KiB. It includes the graph-composition comparisons, complete small Brauer fixtures, regeneration and independent expansion of all local rules, and all 23,040 sampled channel comparisons. It ran single-threaded on CPU7 with 256 MiB address space and a 28-second hard CPU cap. Compilation was separately capped at 512 MiB. The hash/JSON/counter checker used a separate 2-second cap and completed successfully. Conservatively charge the full 30-second review allowance, including metadata and finalization; no further numerical runtime remains authorized.

The producer's recorded Brauer sample times scale to 764.1810277910156 CPU seconds for the three analytic-m actions over all 169,911 origin targets. The tenfold multiplier gives approximately 7,641.81 seconds. This still exceeds the old 180-second gate. The sample alternates Brauer and Cartesian actions with shared source caching; its timing ratio is not a controlled cold-cache speedup. It excludes full GMP moment accumulation, logging/comparison overhead, generic chi/v actions, other sectors, cache construction and the rest of m3/m4. Structural record reductions are exact; projected runtimes are empirical and do not establish intrinsic infeasibility.

The bounds 12816·16·3^15<2^42 for local composition and 2^15·32·15·2^42·3^6·2^33<2^109 for the stated fixed-source action were numerically checked and are mathematically conservative. Checked int64 diagram aggregation and int128 action arithmetic therefore remain within the stated envelope; this does not authorize an unbounded new witness.

The 342,140-byte payload and 1,596,000-byte conservative rule/index charge are not whole-process memory. A whole-moment costed design and any expanded production budget remain separate decisions. No full q6 cache/pass, full 8×4 moment, new .11 energy endpoint or new all-size gap was performed or inferred.

## Reproduction

Preserve source and predecessor seals. Under a newly approved local budget, build the frozen action.cpp with g++ -O2 -std=c++17 -lgmpxx -lgmp (512 MiB build cap). brauer_adapter.cpp changes only the source include location and renames the producer main, preserving the actual algorithms under test. It contains an explicit source path; adjust that path only if reproducing in a different filesystem layout and document the adjustment.

Run the executable with BRAUER_SOURCE_DIR CARTESIAN_SOURCE_DIR FRESH_REVIEW_OUTPUT_DIR, on one core with a 256 MiB runtime cap. It writes regenerated diagrams and fixtures only to the fresh review output. Compare them to sealed files and run the logic in check.py, updating its output path for the fresh location. The sealed setup.py records scaffolding and must not be run over this completed review directory. No production job or additional reference cache is needed.
