# Whole-pipeline measured cost and next decision

The measured schedule evaluates all low-sector expressions plus all 15 signed terms, including Dχ6, generic v/Kv, Cχ6/Cv, analytic m, ψ4, Cm, E†m and χ4 builders. It does not merely extrapolate N/F/L. All eight batches run fresh processes, so each cold phase starts with empty source caches after local operator setup. Repeated phases reuse that batch's capped caches, not a complete production cache.

The 512 cold q6 targets take 4.144846 CPU seconds, and the 128 cold q4 targets take 0.882091. Their mean-rate projection is 1375.497908+30.976555=1406.474463 CPU seconds. Repeated phases take 2.528753 and 0.079137, giving 839.185451+2.779069=841.964520 seconds. These are empirical mean extrapolations, not rigorous time bounds. Cold phase totals 5.344602 and repeated totals 2.740673 include low-q work/checkpoint overhead. Those residuals are 0.317665 and 0.132783 seconds. They cannot be assigned entirely to q2 timing.

The cold phase records 3,745,274 source requests, 4,814,790 diagram hits, 4,335,176 nonzero matching hits, and 164,261 operator calls. The corresponding repeated-only differences are 1,918,003, 2,880,330, 2,536,284, and 45,934. Cold cache hits/misses are 2,526,540/850,160, and repeated-only hits/misses are 1,811,902/175,919. The 10 cold cache clears and 5 repeated-only clears mean the second phase is not fully warm. The m cache is capped at 50000, every other q6 field is independently capped at 50000, and each large q4 field is capped at 4096 (strictly below 4495 origin entries). The peak combined cache contains 60,729 entries. Maximum measured process RSS is 41,604 KiB in the fixtures and 21,368 KiB in the sample.

Cold GMP work takes 0.048525 seconds for 191,621 nonzero Gram products and 318,224 imports. Repeated-only GMP work takes 0.061694 seconds with the same product and import counts. Timing noise and many tiny clock calls make this unsuitable for sub-millisecond attribution. The whole target timing is the better estimator. Reimport across bilinears is not yet optimized.

## Cache setup estimates, explicitly inclusive

Cold miss counts and inclusive builder CPU times are ψ4 32,394/.217866, Cm 8,385/.934147, E†m 128/.023242, χ4 4,283/.580141, χ6 34,610/1.809837, and m 730,839/.506982. These contain recursive dependencies, cache lookup/permutation, and eviction/rebuild effects. They must not be summed as disjoint setup costs or added uncritically to a cold projection that already pays them.

For a candidate separate dense-cache production schedule only, multiply the observed inclusive per-miss rates by 35960 full q4 entries for each ψ4/Cm/E†m/χ4, and 169911 origin χ6 entries. The resulting inclusive upper-style bookkeeping estimates are approximately 0.242,4.006,6.530,4.871,8.885 seconds, and optional analytic m construction 0.118 seconds. They are neither rigorous upper bounds nor validated dense-cache timings. Their sum, roughly 24.65 seconds, deliberately double-counts recursive setup and is a conservative planning allowance only. Dense addressing/storage and complete-fill coverage remain unimplemented.

A cautious whole-job planning envelope is cold joint projection 1406.5 +100 seconds setup/low-q/finalization reserve, then the existing tenfold empirical allowance, giving approximately 15065 CPU seconds. This does not fit a 10800-second cap without reducing that factor or validating optimizations. The repeated-phase estimate plus 100, multiplied by 10, is about 9420 seconds, but is not yet an adequate basis for production admission. Capped warm behavior, dense-cache coverage and restart correctness remain unvalidated. A 1–3-hour run may be plausible after independent review and production hardening. No full job is authorized or launched here.

## Requirements for production use

- No dense cache implementation/coverage bitmap, serialized restart/round-trip, atomic completed-batch protocol or exactly-once resume test.
- No full accepted 8×4 m0/m1/m2 reproduction from this pipeline.
- No separate per-operator timings, per-term GMP counts, or complete target edge/wrap/stabilizer class stratification. m-zero coverage is recorded. Deterministic dispersed indices are retained.
- N/F/L diagram inputs are externally pinned by hash. Production loader does not yet enforce the complete manifest itself.
- Existing generic q6 convention is reproduced with complete small permutation/anchor tests. Production integration is not claimed to reuse its serialized cache implementation.
- Full memory remains a design estimate. Sample bounded unordered maps are not evidence that a full unordered-map cache fits 128/192 MiB. The prior dense-array estimates 75.0 MB without m/95.4 MB with int64 m require actual implementation.

The recommendation is to perform independent fixture/source review first. Then authorize a separately bounded production-hardening gate for dense indexing, input-manifest enforcement, atomic restart/coverage, and cold setup plus whole-target sample comparison. Choose the full CPU/memory budget only after that evidence. Retain the old seals and this sample as references. No gap or endpoint claim follows from this package.
