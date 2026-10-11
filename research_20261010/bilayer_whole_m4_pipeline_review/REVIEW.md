# Independent whole-moment pipeline review

2026-10-11 03:23 UTC / 2026-10-10 23:23 EDT.

PASS for the stated whole m0–m4 algebra, six complete small physical fixtures, and bounded sample provenance. Full 8×4 production admission remains BLOCKED. No complete 8×4 m3/m4, new energy endpoint, or new gap is certified here.

Producer package: ../bilayer_whole_m4_pipeline, manifest SHA256 13010f1d1326fd2c76938036b01ce2e912d70f35714a2c473a529910a790a488. Its complete manifest and four pinned Brauer inputs were checked unchanged. The previous Brauer independent review manifest 2433ba51a63cba8ade95874f3244dea39a7f1acf0bcfe1a327bfb34c1789cfdb was also checked. The 57 coefficients exactly match the N=32 entry of ../bilayer_symmetry_intermediate_points/fixed011_moment_reference.json; geometry and the separate coefficient file match the accepted complete58D review's pinned inputs. Existing sealed files were not altered.

## Independent physical evidence

ALGEBRA.md derives the physical normalization and all high-sector identities, rather than inferring correctness solely from producer output equality. In particular it identifies C as lowering, E as raising, Ed as E† lowering, and derives the essential negative term −<Cm,K Cm>. It proves that q8 and q10 exhaust the high sectors of T²ψ. The 8×4 torus has32 rungs,64 spatial neighbor edges per layer,128 physical intralayer bonds, and Hilbert dimension4^32. The old proposal's “64 rung edges” phrase is a nomenclature error already corrected in the final producer handoff.

The new independent.cpp reference uses dense Cartesian vectors. Its local operator matrices are derived by conjugating the original four-spin swaps, not by calling the producer elementary action, Brauer composition, matching contraction, sparse physical reference, or word compiler. It independently constructs the localized, translation-symmetrized and generic B/L/R/M sources on both4×2 and5×2 tori, including doubled vertical bonds and distinct cR/cM coefficients. It then computes complete χ=Tψ and z=Tχ, without truncating high sectors.

All six cases pass:
- Every coefficient in ψ and the q≤6 χ/z images agrees.
- All fifteen individually signed terms agree with separate dense operator compositions.
- m0,m1,m2,m3,m4 agree with dense ||ψ||²,<ψ,χ>,||χ||²,<χ,z>,||z||².
- Every q≤6 z-sector norm and the complete q8/q10 norms agree. q10 cancels on4×2 and is nonzero on5×2.
- Cm and E†m are independently probed on every q4 support.
- All24 q4 and720 q6 permutations on the selected supports agree with dense χ. Every occupied q6 anchor is checked for χ6 and v on every invariant fixture support.
- All22 scalar accumulators satisfy the exact occupied-origin/full-support identity, using N/q separately by sector, including stabilized supports.
- Both v formulas agree. N→N†, omitting the negative K4 term, omitting either q8 cross, conflating cR/cM, or discarding relevant m-zero targets is detected by the nonzero/difference checks.

The independent executable uses a source adapter that changes only the producer include path and renames its main. The frozen producer source remains in source/. Earlier failed include scaffolding is retained. Do not compile with NDEBUG.

The dense fixtures took9.106213 aggregate wait4 CPU seconds, peakRSS178712KiB, one CPU7 thread, under a256MiB address-space cap. Fixtures/independent.jsonl contains their exact moments and q8/q10 values.

## Integer and GMP review

The frozen c0 is exactly2^48, not strictly less than2^48. The coefficient groups obey |cB|<2^43, |cL|<2^37, |cR|<2^31, |cM|<2^30. This one endpoint correction does not invalidate the producer's broad envelope; the sharper envelope below explicitly uses it.

For the unit-weight8×4 graph, Cartesian row absolute norms of C,C†,D are each at most192<2^8. From the analytic matching formulas, ψ2 amplitudes are<2^43; ψ4 amplitudes are<2^43; matching m coefficients are<2^33 and Cartesian m amplitudes<2^37. There are at most15 matching channels. The implied conservative physical sup-norm bounds are:

- Cm,Dm<2^45; E†m,Km<2^54; x<2^53; γ<2^55
- χ0<2^55, χ2<2^62, χ4/χ6<2^57
- v<2^64; Cv<2^72; Kv<2^81
- Nm<2^63; Fm,Lm<2^72; E Cm<2^62
- D Cm<2^53; K Cm<2^62; every Dχq<2^70
- every low z image<2^76

The formulas are fixed-witness bounds, not permission for arbitrary larger inputs. Distinct-color probes transfer these physical amplitude bounds to the matching coefficients. Every cached/queried source is below2^64.

The review instantiates all large-geometry operators without building a full source cache and verifies their actual record counts and coefficient maxima. Maxima are1 for C/C†/D,3 for K,2 for E/E†,6 for N/N†,48 for F,36 for L; every operator has fewer than2^15 records. A target action has at most32 translated copies per record,15 input matching channels and3^6 closed-loop amplification. Thus the absolute sum of all diagram intermediates is bounded by

2^64 × 2^15 ×32 ×15 ×64 ×3^6 <2^104.

The separated vacuum inclusion–exclusion path has at most2^5 subsets per local block and fits a smaller bound. Its int64 coefficient accumulation is safe; the full source action remains far inside signed int128. This supplies a partial-sum bound stronger than the producer's final-image-only table. Checked arithmetic still guards actual action additions/products; direct analytic source operations are within their explicit coefficient bounds.

All scalar norms/bilinears, term weights and moment assembly use GMP. Signed two-word conversion was independently checked at0,±1,±2^100 and near±2^126; there is no narrowing through long. Reported sample maximum of two limbs concerns imported vectors/bilinears, not every final accumulator. Fixture values are unnormalized T moments; normalized H′ moments divide by ||ψ||²200^k.

## What the bounded8×4 evidence establishes

The producer's successful disjoint samples cover exactly512 q6 indices and128 q4 indices in each cold/repeated phase, plus64 q2 and vacuum in the first batch. The review independently verifies support index validity/uniqueness, all496 q2 rank round trips in the saved checks, source/executable hashes, and equality of all fifteen terms and all five scalar expressions between each batch's cold/repeated outputs. Those are partial mixed-sector scalar sums, never full physical moments.

An additional review replay completed64 q6 and16 q4 cold target steps. Its saved64-q6 checkpoint agrees exactly with the corresponding producer checkpoint. The3-second reservation has an internal CAP−2 soft limit; the replay reached that soft stop during low-sector work at1.210346 aggregate wait4 CPU seconds and did not reach the repeated phase or produce final scalar totals. It was not retried. The16 q4 steps have timing/coverage records but no completed aggregate checkpoint, so they are not presented as independently verified q4 scalar totals. Independent8×4 repeated-phase execution is therefore not established by this review; its equality is inspected producer evidence. This limitation does not weaken the complete dense physical fixture comparisons above.

## Cost and production gate

This is a whole-step sample: it includes generic dense χ/v, Dχ, Kv, all fifteen GMP terms and lazy source construction. It is not the earlier three-operator m-only estimate. The producer cold q6/q4 mean-rate projections sum to1406.474463 CPU seconds; repeated projections sum to841.964520. The review recalculates these from the raw target rows.

Cold misses include construction of ψ4,Cm,E†m,χ4,χ6 and analytic m. Their builder timers are recursively inclusive; they cannot be added as disjoint stages. Their proposed roughly24.65-second dense-setup extrapolation uses the full35960 q4 and169911 q6 cache sizes, but remains unvalidated: no dense addressing/fill implementation exists in this package. Cold and repeated phases contain10 and5 cache clears respectively, so the latter is not a complete-cache warm benchmark. Sample RSS is not a full-cache memory bound. Per-operator attribution, per-term GMP attribution and complete edge/wrap/stabilizer stratification remain missing.

The cold planning envelope (1406.5+100)×10≈15065 CPU seconds exceeds10800. The repeated envelope≈9420 cannot substitute without a validated production schedule/cache setup. These are empirical planning numbers, not rigorous runtime bounds or an intrinsic impossibility result. No full production budget is approved by this review.

Production also needs input-manifest enforcement, atomic exactly-once checkpoints and coverage, a tested interrupted/resumed round trip, final exact q-sector weights, and complete m0/m1/m2 agreement with accepted matrices. The parent has separately authorized a bounded hardening gate; that future package and its guard tests require their own review. No additional numerical work remains under this review's90-second ledger.

## Resource findings and failures retained

Producer numerical wait4 total26.904021 seconds and conservative charge257/300 are consistent with the saved ledger; the failed35-second sample reservation remains charged. Compilation CPU was not recorded by the producer, and early fixture launches lack source/executable hashes. Neither fact is silently upgraded to verified historical provenance.

The producer's /proc/<pid>/task/<pid>/children path is absent in this environment. Its try/except silently skips descendant detection. Direct-child CPU, wall limits, process-group kill and wait4 records remain present, and the mathematical executable has no subprocess-launch path, but general process-tree enforcement is NOT VERIFIED for that frozen producer guard.

The review encountered the same missing path during its first, failed include compilation. That attempt is charged20 seconds; actual wait4 was6.378730. After notifying the parent and receiving permission, the review guard was repaired to scan numeric /proc stat PPid/process-group fields. It uses a child subreaper to account and reap orphan descendants, monitors aggregate live/reaped CPU and RSS, keeps an external wall watchdog, and fails on observation errors. A real spawned-descendant self-test detected both CPU7 processes, killed the group, reaped the orphan and verified no live group remained; it charges3 seconds, actual0.044175.

A corrected-O2 build was stopped by the aggregate CPU guard at19.056706 seconds, with no orphan left, retaining its20-second charge. The parent authorized one final-O1 attempt, which passed13.888050 CPU seconds under15 seconds, observed three processes, aggregate observedRSS424194048 bytes<512MiB, peak processRSS413484KiB. No further build retry occurred. The direct fixture run charges25 seconds, the partial sample3, and hash/final checks4. Total charge is90/90, actual aggregate wait4 across these attempts is49.784555 seconds. The first compile's general tree observation is explicitly unverified; the repaired observer and later cap/cleanup paths have positive tests. Live-plus-reaped sampling may conservatively double count around a reap race; final charging uses wait4 and never refunds reservations.

## Reproduction

Use a fresh directory and a newly authorized budget. Compile independent.cpp with g++ -O1 -std=c++17 -lgmpxx -lgmp; -O2 exceeded this review's build allowance. Run independent OUTPUT RULE_DIRECTORY SOURCE_INPUT_DIRECTORY under a single-CPU runtime guard. The executable also supports the producer's sample argument layout. guard.py is parameterized for CPU/time/memory caps but deliberately fixes this review's90-second ledger and CPU7: copying it for another authorized task requires an explicit new ledger and documented caps. Do not rerun it against this sealed review directory.
