# Exact q8 norm reduction by the hard-core pair commutator

2026-10-10 17:41 EDT / 21:41 UTC.

The local analytic proof and independent exact checks on small fixtures passed. The work includes no large production contraction and establishes no new physical gap or denominator endpoint.

The missing q8 Gram can be computed with only q4/q6 contractions.

    (A86 M)* (A86 M) = (CM)* (CM) + M* [C,C†] M.

PROOF.md fixes the spherical spin convention, identical/overlapping-edge signs, ordered-wedge factors, repeated-edge weights and matching implementation. COST_PLAN.md gives a streaming implementation plan, exact support counts and resource gates, starting with 8×4 rungs (64 physical spins).

verify.py is independent of all project producer code. It reconstructs the local A=2V from physical spins, exhaustively tests the local and weighted graph identities, and compares all entries against explicit q8 images on 2×2, 3×2 and 4×2 physical fixtures. TEST_RESULTS.json and test.log preserve the observed execution. REPRODUCE.sh reruns under one CPU (CPU6), single-thread BLAS and a 1 GB virtual-memory cap. It prints results without changing sealed artifacts.

The 4×2 coherent fixture has a nonzero q8 norm 3,898,368. Its commutator contribution is negative, −14,807,040, so hard-core occupied-center terms cannot be discarded. A saturated 3×2 fixture checks cancellation to zero.

The separate full-residual assessment must also handle q4/q6 image norms. In particular ||A64R+A66M||² cannot be restricted to M-active q6 supports. On 8×4, the conservative full fixed-origin q6 set has 169,911 supports, versus 73,206 for M. The present result supplies the exact q8 reduction.

Artifacts are content-sealed by MANIFEST_SHA256.json. verify_seal.py checks every recorded file. INPUT_SHA256.json records the prior sources consulted, without importing or changing them. New work or benchmark outputs should go in a new directory, leaving this seal intact.
