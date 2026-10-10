# Complete 8×4 bilayer residual: independent review

Updated 2026-10-10 17:53 America/New_York (EDT) / 21:53 UTC.

PASS: ordinary periodic spin-1/2 square bilayer at g=1/10 has a unique ground state and gap at least **0.038976038275** for every integer square side L≥2.

The new ingredient is a complete exact residual for one rational vector from the 43-dimensional 8×4-rung singlet search. Its full space is 2^64. The q8 contribution is evaluated exactly with the hard-core commutator, without production q8 enumeration. The complete positive variance is approximately 0.0003553876503424027; the justified ground lower is approximately −0.2532914854282799. The denominator still retains 97 levels, and the largest numerator uses one previously accepted 8×8-rung trial state from a 43D search (full space 2^128).

Read REVIEW.md for the proof, provenance, arithmetic bounds, support audit and exhaustive size coverage. Exact outputs:

- local_result.json: independent physical commutator and tiny fixtures
- independent_8x4.json: all fresh q4/q6/commutator contractions
- assembly_result.json: exact positive full variance and sector Temple bound
- scalar_result.json: exact trace ratios, all finite windows and all-integer bootstrap
- polynomial_result.json: accepted fixed-vector coupling polynomial export

Run bash REPRODUCE.sh with GMP development libraries and Python SymPy available. It uses CPU6, one numerical-library thread, and a 1 GiB address-space cap. No producer module is imported; only hash-pinned independent scalar arithmetic is reused. All writes stay in this review directory.

This is a discrete g=.10 gap certificate. The separately accepted polynomial export does not itself certify a continuous coupling interval. No q8 production enumeration, new largest-seed residual, all-temperature exclusion, or optimality claim is made.
