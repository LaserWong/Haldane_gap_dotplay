# Uniform-chain coverage from L26

2026-10-10 22:29 EDT / 2026-10-11 02:29 UTC. This exact producer result awaits review.

The length-resolved certificates give a unique ground state and gap≥.0023 for every integer L≥26. Parity-dependent checks cover 26 and 27, and the frozen n28 result covers larger lengths. Bootstrap initialization remains 30. Stronger bounds starting at 28/32/34 are retained.

A uniform-window attempt over 26..52 failed before the length-dependent refinement succeeded. `PROOF.md` explains the distinction. `certificate.json` preserves the failed attempt, and `length_resolved_certificate.json` records the positive result. Replay with `python certify.py` followed by `python certify_missing_lengths.py`. No n24 calculation or minimum-seed claim is included.
