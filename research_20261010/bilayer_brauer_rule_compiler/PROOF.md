# Invariant local algebra, exact validation and sample

## Representation and composition

For a support of at most five rungs, a diagram stores two five-bit occupation masks and a pairing of the occupied external color legs. Incoming legs use positions 0..4 and outgoing legs 5..9; unused positions carry nibble 15. The key uses forty pairing bits followed by incoming/outgoing masks. A signed int64 coefficient multiplies the product of Cartesian Kronecker deltas along the pairs.

Elementary C† pairs the two newly occupied outgoing legs. C pairs the two incoming legs being annihilated. D hopping joins the incoming occupied leg to its new outgoing site. D on two occupied triplets is the crossed propagation diagram minus the product of incoming and outgoing pair contractions. Spectator occupied sites propagate through identity pairs. These are the direct Cartesian edge conventions, not spherical color indices.

Composition first checks intermediate occupation equality. A union-find structure glues the diagrams on three layers (initial, intermediate, final) of at most five sites. Components with two external ends become output pairs; components without external ends contribute a factor of three. Any other external degree fails an assertion. The all-vacuum identity is handled with no color loop. Signed coefficients are collected exactly after every letter and word. The generator reuses connected, ordered, signed word enumeration with repeated edges and safe disjoint-letter commutations from the accepted compiler.

This pairing representation need not be linearly independent at O(3) rank eight/ten. Only identical diagram keys are combined; no minimum-basis claim is made. Overcompleteness is harmless for correctness because all final Cartesian matrices are checked exactly.

## Complete local comparison

Each diagram is expanded by assigning one of three colors to each paired external component. Source/target local state indices are constructed from those assignments and signed coefficients collected. For every canonical support in N/F/L, this entire sparse matrix equals the sealed Cartesian matrix loaded from rules_N/F/L.bin. This checks all nonzero entries and omitted zeros, implicitly 1270272/59990528/59990528 entries, or 121251328 total.

The resulting counts are:
- N: 634 diagrams on 27 support blocks; maximum absolute coefficient 6
- F: 14532 diagrams on 83 blocks; maximum coefficient 48
- L: 1941 diagrams on 83 blocks; maximum coefficient 36

Each serialized record is uint32 support, uint64 pairing/mask key, int64 coefficient, written separately in little-endian host order for 20 bytes. Total payload is 342140 bytes. The cumulative runtime gate charges 32 bytes per diagram plus a 1 MiB index allowance and aborts above 16 MiB. Actual charge is 1596000 bytes. This charge is a record/index budget, not whole-process RSS; compiler reference matrices, temporary maps, source cache and runtime storage are covered by the separately enforced 256 MiB address-space limit. Whole-run measured RSS is 28032 KiB.

## Translation and stabilizers

Ordered tuples are anchored once by the designated first edge, whose 8×4 translation orbit has 32 members. Endpoint permutations are carried into the canonical support. Every compiled block is applied at all 32 translations; no second division by 32 occurs.

The new compiler explicitly counts support-preserving translations. Each family has one support block with stabilizer order four; every other support has order one. All embeddings, including equal support masks with different local permutations, are retained. Exact equality to the accepted local Cartesian matrices and the full sampled action comparisons preserve the predecessor's stabilized Hermitian F/L sums. N is not assumed Hermitian. Neither graph-isomorphism nor point-group compression is introduced.

## Small physical validation

The small graphs are recompiled from full unquotiented connected tuples, with their actual doubled width-two edges. Expanded Brauer matrices act on the entire q6 fixture vector. N m, F m and L m agree exactly with direct nested physical Cartesian operators on both 4×2 and 5×2. The resulting full vectors are also reconstructed from the fifteen invariant probes to check matching-channel extraction.

The physical fixture is replayed and its complete moment/sector outputs and all fifteen signed terms match the sealed Cartesian predecessor exactly. In particular the 5×2 q10 contribution is nonzero and the 4×2 cancellation survives. The physical 16×16 edge derivation and the identity 15×15 probe matrix are rechecked at process startup. Small reference q8/q10 vectors are allowed only on eight/ten rungs; none is constructed on 8×4.

## Matching-channel action

For each target support, an occupied-site incidence index selects each touching embedding once, using its smallest occupied intersection site. Its local target occupation mask selects a row of diagrams, with no target-color probes or matrix-unit scan.

A diagram's input mask determines the six-site source support after spectators are preserved. The fifteen analytic source channels are fetched together. Exactly zero source tensors may be skipped; target supports are never excluded because m vanishes there. The source is the same accepted m=M cM and full-support-keyed, 16384-entry capped lazy cache used in the Cartesian package.

For every nonzero source matching, join its six incoming legs with the diagram and spectator identity lines in a second union-find calculation. Closed components contribute three; the six outgoing legs form a unique output matching. Accumulate the signed coefficient in that channel. This is a direct invariant tensor contraction; there are no color assignments or Gram inversion in the action.

Local vacuum projectors are separated and expanded into occupation-subset polynomials, exactly as in the Cartesian implementation. Nonempty subsets are indexed by their smallest site; the scalar constant is handled once. The independently loaded Cartesian action checks vacuum contributions through direct geometry and supplies a complete per-channel reference.

## Checked bounded sample

The targets are the same 512 distinct origin-containing supports with colex ranks floor(j·169910/511). All three families complete every target. For each target, the fifteen Brauer outputs equal the fifteen Cartesian outputs exactly, giving 23040 coefficient equalities. The reference action loads the sealed Cartesian matrix-unit files and retains its different color/probe method; it does not call the Brauer composition code. The two methods share the already validated analytic source kernel and capped source cache.

N/F/L diagram hits are 264312/1717692/683326; nonzero-source diagram hits are 118919/811151/325302; individual nonzero source-matching contractions are 194974/1406007/528154. The source-request counters exclude the one initial target-source fetch per support. There is no full q6 cache or traversal of all 169911 targets.

Action CPU times for 512 targets are .200126/1.63998/.462633 seconds. The contemporaneous Cartesian reference times are 1.1461/8.83703/2.67404 seconds. These actions alternate and share a cache, so the ratio is not a controlled independent cold-cache speedup. The previous standalone Cartesian sample totals also differ. Structural record/hit reductions are exact; timing extrapolations are empirical.

Compilation and local-matrix comparison of the three 8×4 families take .086453/.567082/.176029 CPU seconds in this run. Sample action timings exclude output logging, per-channel comparisons and any full-moment GMP accumulation. No full-moment cost is inferred from this narrow measurement.

## Arithmetic and resource limits

Pairing composition can have at most fifteen intermediate occupied vertices in a length-four five-rung word; the deliberately loose 12816·16·3^15 coefficient envelope is below 2^42. Composition coefficients and their map accumulations use int64 storage with int128 checked additions. Local expansions fit int64 under the same absolute expansion envelope. Measured final coefficients are at most 48.

For the fixed source, each matching channel is below 2^33. A coarse matching-action bound uses fewer than 2^15 diagrams, 32 translations, 15 source channels, coefficient bound 2^42, at most six closed source-color loops, and source bound 2^33; this is below 2^109, inside signed int128. The known small physical fixture uses checked int64 amplitudes and int128 inner products. These bounds do not authorize reusing the kernel for an unbounded new witness.

Runtime was limited to 60 CPU seconds, CPU6, one thread, 256 MiB address space. Soft compiler checkpoints stop above 55 seconds, and sampling stops before starting another target once cumulative CPU exceeds 52 seconds. The first launcher failed before executing the numerical program because /usr/bin/time was absent; launcher_unavailable.log retains that fact. A Python rusage wrapper then ran the program once and measured 19.577705 user plus .532573 system CPU seconds, exit status zero. Bounded postprocessing used .084718 CPU seconds. No runtime restart, hardening replay or budget increase occurred.

## Result and next boundary

Mean scaling of these three m-source actions to all 169911 origin targets is 764.181 seconds, or 7641.810 seconds with a tenfold multiplier. Thus the old 180-second resource proposal still fails. This neither proves fundamental infeasibility nor forbids a future explicitly approved larger allocation.

Generic chi/v action, remaining low-sector terms, cache setup and full GMP contractions are not priced here. A whole-m3/m4 costed implementation plan with exact small fixtures and a bounded whole-moment sample is needed before any proposal for a full job. No full physical moment, improved endpoint or new gap certificate is asserted.
