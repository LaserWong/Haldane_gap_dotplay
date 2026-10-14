# Exact pi-current improvement and specified-recipe exclusion

For the uniform periodic spin-1 Heisenberg chain, the fixed archived D = 26 state at n=24 has a compact two-vector pi trial span:

- v=sum(-1)^j S_j^+/sqrt2 psi
- w=[H,sum(-1)^j S_j^+/sqrt2] psi

Exact contractions improve its first Rayleigh difference from psi from 0.4910226055 to 0.4238202243. A second exactly Gram-orthogonal rational direction has difference 3.8268850622. Neither number is an asserted physical eigenvalue. The two-vector linear search is distinct from the individual MPS bond bound 156.

The improved 70-state lower trace (or 73-state trace keeping both triplets) excludes every beta>=0 for the fixed D = 26 length 48 single-Rayleigh numerator and the specified thermal-first / delayed joint-aware canonical recipes. All 318 closed boxes covering [1/2,80] and both tails pass exact directed arithmetic. This does not exclude new interpolation lemmas or other uses of the same physical data, and does not assert physical gaplessness or a universal minimum seed size. Earlier weaker-screen windows are preserved unchanged.

Files:

- PROOF.md: local current, wrap, source cells, H insertions, orthogonality, spin completion, exact scalar coverage, and scope
- PHYSICAL_MANIFEST_SHA256.json: frozen 74 integer C/K values and checkpoint
- SCALAR_MANIFEST_SHA256.json: frozen exact 2x2 forms, rational vectors, trace groups, and all-beta scalar certificates
- pi_two_vector_results.json: Gram/H, exact vectors, norms and Rayleighs
- pi_scalar_results.json: complete rational box histories for 70/73 states
- INPUT_MANIFEST_SHA256.json: immutable implementation and fixture inputs

The n24 run cost 795.06 CPU seconds, 266.70 MiB, one core. Cell construction cost 25.61 CPU seconds. The final two scalar screens cost 44.83 CPU seconds /10.25 MiB. The physical campaign is complete. Do not rerun it in this frozen directory. Independent review writes only to the sibling mps_commutator_review.

For replay, copy this assessment and its sibling mps_excited_seed_witnesses to a fresh research directory, preserving their relative paths. Run `taskset -c 2 python3 fused_current/assemble_pi.py` and `taskset -c 2 python3 fused_current/verify_pi_scalar.py` from the copied assessment. These scripts write outputs. Never run them against the freeze. Physical fixture replay uses verify_tiny_commutator.py and fused_current/verify_fixtures.py in that copy. Rebuilding the C++ engine uses `g++ -O3 -std=c++17 contract_current_cached.cpp -lgmpxx -lgmp`. The complete n24 checkpoint makes run_n24_checkpointed.py a no-op. A fresh large replay must use a new output tree and obey its measured resource gate.
