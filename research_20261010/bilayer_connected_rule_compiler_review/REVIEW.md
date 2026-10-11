# Independent connected-rule compiler review

2026-10-11 02:11 UTC / 2026-10-10 22:11 EDT.

**PASS for the frozen local operator algebra and bounded fixture scope.** No production-feasibility or new spectral-gap claim. Reviewed ordinary isotropic bilayer conventions H′=Q+(g/2)(C+C†+D), N=[C,[D,C†]], F=[[C,D],[D,C†]], L=[[C,[C,C†]],C†].

## Seal provenance

Requested initial manifest seal: `ca4e1e0ae113d6e2fea60e694fa5e6735443f4e688a6168b39c8f758977c6d19`.
Current final manifest seal: `e165f87b117e229c957e07f54151fab9c2798c31db961568bd3589ee900e2e66`.

This is an explicit, verified change of target, not a silent substitution. The producer explained that only PROOF.md's conservative small-graph tuple estimate changed `10·7·13·19` to `15·7·13·19` because the 5×2 graph has 15 distinct weighted edges. Reversing that exact substitution independently produces original PROOF hash `3e5e589be090f6fab992b2e35423c61da7e8e834cdb4901d2fa5f9e2936c82d5`; replacing only that manifest entry independently reconstructs the original announced manifest SHA. All code, rules, fixtures, and counts are consequently identical between the two manifests. Every final manifest entry and every pinned input-manifest hash was verified. The exported project has no .git directory; no commit or remote change was performed.

## Independent full local comparison

`independent.cpp` does not include producer code. It separately expands oriented brackets, groups by translated support, and evaluates unreduced words using an independently derived physical edge table. It deliberately does not implement the producer's trace-monoid simplification. It compares every nonzero matrix element, in serialization order, against the frozen binaries and checks every omitted zero. Elementary action is certified independently from the four-spin Hamiltonian 2(Sa1·Sb1+Sa2·Sb2) by exact rational arithmetic in `exact_edge.py`; the preliminary numerical transform is not the acceptance criterion.

- N: 134 anchored tuples, 27 supports, 6,800 records, 1,263,472 omitted zeros, 3,484 negative records
- F: 1,242 anchored tuples, 83 supports, 255,819 records, 59,734,709 omitted zeros, 128,430 negative records
- L: 1,602 anchored tuples, 83 supports, 34,618 records, 59,955,910 omitted zeros, 17,603 negative records

Total: 297,237 records; 3,566,844 bytes; 121,251,328 checked implicit matrix entries. Independent reconstruction took 2.13336 CPU seconds, peak RSS 3,328 KiB. This verifies cancellations and signs without relying on the producer's two evaluators sharing an elementary action.

## Translation and stabilizers

The independent enumeration verifies all 64 undirected edges each have 32 distinct translations. The positive vertical and horizontal edges at 0 therefore provide one representative of each edge orbit. For each ordered connected tuple its designated anchor uniquely fixes its translation representative. The non-anchor letters retain their order and orientation. For F, both internally touching pairs are enumerated and only their unions must touch; no incorrect third-edge prefix restriction is imposed.

Support canonicalization picks the least translated bitmask and translates every site in every word with that same map. Ties select one map, which is harmless when all 32 translated embeddings are restored. In each family exactly one support has translation stabilizer 4; the remaining 26/82/82 have stabilizer 1. There is no further support-stabilizer division: the quotient was on an anchored ordered tuple, whose action is free, not on an unlabelled support. Thus there is also no second /32 factor. Point-group orientations are retained.

A direct independent Cartesian whole-operator vacuum test on 8×4 gives N=-384, F=4992, L=-7104. Each is exactly 32 times the sum of its stored vacuum-diagonal coefficients. This checks actual translated embeddings including the stabilizer case and normalization. It is a vacuum-only test (temporary intermediate sectors at most q4), not an 8×4 q6 witness or production support contraction.

## Cartesian fixture check

`cartesian_fixture.cpp` preserves the accepted fixture's test vector coefficients, normal-order formulas, and output schema, but replaces all elementary C/C†/D and pair-creation actions with independently implemented Cartesian delta actions: pair creation/annihilation is delta; D swaps a singlet/triplet and on two triplets acts as permutation minus delta contraction. Thus the global action is independently implemented, while the formulas under test are intentionally the same formulas. Both 4×2 and 5×2 weighted periodic graphs retain doubled vertical bonds.

Both Cartesian runs reproduce all 15 signed terms, direct and normal-ordered m3/m4, all sector norms, and scalar diagnostics exactly. The sole omitted metadata comparison is peak sparse-state count, which is basis-dependent. Negative F expectations, nonzero L terms, oriented cross terms, 4×2 q10 cancellation and positive 5×2 q10 remain tested. Runtime wall upper bound 0.571 seconds and peak RSS 6,852 KiB.

The source production rules remain spherical (s,t+,t0,t−). The Cartesian triplets can be chosen x=(-t++t−)/√2, y=i(t++t−)/√2, z=t0, giving the positive delta pair. The 15 matching probes are valid only for a Cartesian rank-six invariant tensor in the delta-pairing span; equal spherical digit values cannot be used as Cartesian colors. Neither this review nor the fixture check supplies a production Cartesian pull index or a full basis-transformed production payload.

## Authoritative evidence and limitations

The authoritative source package run/counts.json and run/checkpoint.json report a complete 3.46989-CPU-second run at 5,120 KiB RSS. This review corroborates its content, not that timing on another machine. The optional checkpoint-hardening replay remains INCOMPLETE_CPU_CAP. Byte identity of its rules does not promote its incomplete counts/report to acceptance. The completed source was restored before sealing. Aggregate checkpoint fields expanded words/vacuum/max coefficient are misleading zeros due to an acknowledged bookkeeping omission; per-family counts are authoritative and correct. This is a nonblocking reporting defect for the sealed local algebra.

No full 8×4 q6 state/cache, production contraction, global 8×4 q8/q10 enumeration, 8×8 run, or new gap was performed or authorized. A full indexed Cartesian sample or production step still needs its own resource gate. The source REPRODUCE.sh replays producer code and is useful for byte reproducibility; independent review reproduction is below.

## Reproduction and resource bounds

Use a fresh output directory; leave the producer package immutable. Set single-core CPU7 and RLIMIT_AS 256 MiB for runtimes, 512 MiB separately for C++ compilation. No OpenMP/BLAS worker expansion. Build independent.cpp, cartesian_fixture.cpp and vacuum.cpp using g++ -O2 -std=c++17. Run prepare.py first to verify source hashes and prepare edge_table.txt, then exact_edge.py for exact acceptance; run independent with arguments REVIEW_DIR SOURCE_DIR; run cartesian_fixture with a fresh output directory and compare the fixture and terms JSON to SOURCE_DIR/validation, removing only peak_sparse_states; run vacuum and compare to 32 times each binary's src=dst=0 coefficient sum. make_cartesian.py reproduces the Cartesian source alteration and independently reconstructs the old seal. Avoid executing it in the frozen review directory.

The review's five numerical runtime caps were 3,12,5,3,3 CPU seconds, totaling 26 seconds, each at 256 MiB on CPU7. All completed successfully, far below their caps. Charge the full 30-second review allowance conservatively, including metadata checks and tiny finalization tails; no numerical budget remains. One failed initial C++ build was corrected before any independent executable ran; builds were separately 512-MiB capped and excluded from runtime accounting. No producer numerical run was repeated. Any fresh reproduction requires a new local-algebra allowance.
