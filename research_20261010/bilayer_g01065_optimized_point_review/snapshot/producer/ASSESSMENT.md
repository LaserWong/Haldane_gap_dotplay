# Cached-matrix optimized g=.1065 point

Updated 2026-10-11 00:50 UTC / 2026-10-10 20:50 EDT.

The first requested coupling,213/2000=.1065, gives the exact candidate

 gap >= 5362952719/250000000000 = .021451810876

for every integer periodic square L>=2, with unique finite-volume ground state, pending independent review. Initial beta189/20=9.45. Four exact windows cover[8,16],[16,32],[32,64],[64,128], and the canonical asymptotic theorem starts at128. The previously accepted short[0,.15] theorem covers L2,...,7 with a larger gap. This is a point certificate, not a coupling-interval claim.

The authorized stopping condition was the first positive exact candidate, so **.10675 and .107 were not tested**. No higher-coupling or optimal-frontier conclusion is made.

Energy optimization and complete Temple-pencil optimization were compared in the accepted21D4x4 and57D8x4 spaces. Floating generalized eigenvectors only propose rational coefficient vectors (integer grid2^48); every norm, mean, complete second moment, variance, negative pencil witness, global-ground margin and sector cutoff is recomputed exactly. The complete matrices include every q8 term. No support contraction or new matrix element is computed.

Both patches select their Temple-pencil vectors. At4x4 its ground lower is about-.14437423843187203, improving the energy-vector Temple lower by6.1019435e-7. At8x4 it is about-.28840195137761737, improving by4.7407802e-5. These are finite rational witness gains, not proofs of globally optimal21D/57D endpoints. The old g=.11 positive-pencil exclusions apply to specified .11 targets and do not exclude these new .1065 vectors or cutoffs.

The numerator uses an energy-optimized rational vector in the already accepted43D8x8 mean/Gram space and retains one state, without requiring its residual. The two denominator low-band counts remain49/97, despite ground search dimensions21/57; the combined ground-plus-odd trial dimensions are69/153. The largest physical Hilbert dimension is2^128. Fixed z=.1 odd full-moment polynomials, reference floors, global count gates and every omitted tail term are checked at the new coupling.

result.json includes both rational vectors per denominator, every exact matrix witness, complete coupling polynomials for those fixed vectors, the numerator vector and affine mean, physical trace data, the best exact candidate and diagnostic proposal counts. candidate_g01065.json isolates the certificate. Direct dependencies and independent matrix reviews are pinned in INPUT_SHA256.json and result.json.source_seals.

All scalar acceptance uses directed384-bit exponentials, rational rounding, integer-square-root enclosures and exponential gap witnesses. The finite beta grid7..14 by.05 found54 proposals and selected9.45; it does not establish a global optimum. Single CPU2,256MiB hard cap,115CPU-second internal cap within the separately authorized120-second allocation. Initial and final coefficient-preserving replays each took about4CPU seconds and53MiB. No predecessor, project-root or GitHub file changed. The separately authorized closed[.106,.1065] extension must be a new immutable package.
