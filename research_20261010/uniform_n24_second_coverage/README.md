# Individual probes at sizes 24 and 25

2026-10-10 22:32 EDT / 2026-10-11 02:32 UTC. These producer results await review.

- L24 has an exactly certified unique ground state and gap>=.0023.
- At L25, the current lower-purity bound .3734591 fails to give a positive certificate.
- Contiguous coverage remains L>=26, and the bootstrap initialization remains 30.

A finite cooled grid tested 511 legal candidates without success. This is neither a minimum-size theorem nor a no-go theorem. The work used its own fresh MPS48 input, with no n22 calculation or new thermal work. PROOF.md and length_resolved_certificate.json give the details. Replay certify.py followed by certify_missing_lengths.py.
