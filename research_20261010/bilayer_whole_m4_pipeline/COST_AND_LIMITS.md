# Whole-pipeline measured cost and next decision

The measured schedule evaluates all low-sector expressions plus all15 signed terms, including Dχ6, generic v/Kv, Cχ6/Cv, analytic m, ψ4, Cm, E†m and χ4 builders. It does not merely extrapolate N/F/L. All eight batches run fresh processes, so each cold phase starts with empty source caches after local operator setup. Repeated phases reuse that batch's capped caches, not a complete production cache.

512 q6 cold targets take4.144846 CPU seconds;128 q4 cold targets take0.882091. Their mean-rate projection is1375.497908+30.976555=1406.474463 CPU seconds. Repeated phases take2.528753 and0.079137, giving839.185451+2.779069=841.964520 seconds. These are empirical mean extrapolations, not rigorous time bounds. Cold phase totals5.344602 and repeated totals2.740673 include low-q work/checkpoint overhead; those residuals are0.317665 and0.132783 seconds. They cannot be assigned entirely to q2 timing.

Cold source requests3,745,274; diagram hits4,814,790; nonzero matching hits4,335,176; operator calls164,261. Repeated-only differences are1,918,003;2,880,330;2,536,284;45,934 respectively. Cold cache hits/misses2,526,540/850,160. Repeated-only hits/misses1,811,902/175,919. Cold clears10 and repeated-only clears5 mean the second phase is not fully warm. m cache is capped at50000, every other q6 field independently capped at50000, and each large q4 field4096 (strictly below4495 origin entries). Peak sum of cached entries60,729; maximum measured process RSS41,604KiB occurs in fixtures, sample maximum21,368KiB.

Cold GMP0.048525 seconds,191,621 nonzero Gram products,318,224 imports. Repeated-only GMP0.061694 seconds with the same product/import counts. Timing noise and many tiny clock calls make this unsuitable for sub-millisecond attribution; the whole target timing is the better estimator. Reimport across bilinears is not yet optimized.

## Cache setup estimates, explicitly inclusive

Cold misses and inclusive builder CPU: ψ4 32,394/.217866; Cm8,385/.934147; E†m128/.023242; χ4 4,283/.580141; χ6 34,610/1.809837; m730,839/.506982. These contain recursive dependencies, cache lookup/permutation, and eviction/rebuild effects. They must not be summed as disjoint setup costs or added uncritically to a cold projection that already pays them.

For a candidate separate dense-cache production schedule only, multiply the observed inclusive per-miss rates by35960 full q4 entries for each ψ4/Cm/E†m/χ4, and169911 origin χ6 entries. The resulting inclusive upper-style bookkeeping estimates are approximately0.242,4.006,6.530,4.871,8.885 seconds, and optional analytic m construction0.118 seconds. They are neither rigorous upper bounds nor validated dense-cache timings. Their sum, roughly24.65 seconds, deliberately double-counts recursive setup and is a conservative planning allowance only. Dense addressing/storage and complete-fill coverage remain unimplemented.

A cautious whole-job planning envelope is cold joint projection1406.5 +100 seconds setup/low-q/finalization reserve, then the existing tenfold empirical allowance: approximately15065 CPU seconds. This does not fit a10800-second cap without reducing that factor or validating optimizations. The repeated-phase estimate plus100, multiplied by10, is about9420 seconds, but is not an adequate production admission basis yet: capped warm behavior, dense-cache coverage and restart correctness remain unvalidated. A1–3-hour run may be plausible after independent review and production hardening; no full job is authorized or launched here.

## Missing readiness evidence

- No dense cache implementation/coverage bitmap, serialized restart/round-trip, atomic completed-batch protocol or exactly-once resume test.
- No full accepted8×4 m0/m1/m2 reproduction from this pipeline.
- No separate per-operator timings, per-term GMP counts, or complete target edge/wrap/stabilizer class stratification. m-zero coverage is recorded; deterministic dispersed indices are retained.
- N/F/L diagram inputs are externally pinned by hash; production loader does not yet enforce the complete manifest itself.
- Existing generic q6 convention is reproduced with complete small permutation/anchor tests; production integration is not claimed to reuse its serialized cache implementation.
- Full memory remains a design estimate. Sample bounded unordered maps are not evidence that a full unordered-map cache fits128/192MiB. The prior dense-array estimates75.0MB withoutm/95.4MB with int64m require actual implementation.

Recommendation: independent fixture/source review first. Then authorize a separately bounded production-hardening gate for dense indexing, input-manifest enforcement, atomic restart/coverage, and cold setup plus whole-target sample comparison. Choose the full CPU/memory budget only after that evidence. Retain the old seals and this sample as references. No gap or endpoint claim follows from this package.
