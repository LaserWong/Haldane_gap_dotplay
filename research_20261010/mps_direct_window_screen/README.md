# MPS inputs under the direct-window route

Exact necessary screening excludes the specified scalar route for every
separately checked even n=6,...,24, with the fixed D26 numerator at 2n.
At n24, the 70/73-state lower traces still prevent closure even when all
finite-size bridges are optimistically granted. The new direct-window
lemma alone therefore does not rescue these fixed inputs.

This is not a gap certificate, a physical-gaplessness statement, or a
universal minimum seed-size result. Different recursion/closure formulas
and different numerator inputs are outside scope. Earlier freezes remain
unchanged. See PROOF.md for exact route, physical indexing and limitations.

- exact_results.json: exact inherited beta coverage and all delayed paths
- verify_relaxed_paths.py: 0.25-CPU-second directed-rational replay
- bounded_scan.json: separate floating proposal diagnostic
- MANIFEST_SHA256.json: immutable producer artifact hashes

The test uses the existing physical inputs without new contractions or support expansion. Its scalar conclusions require a separate independent review, which can use the existing physical seals.
