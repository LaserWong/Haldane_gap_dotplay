# Optimize cooled uniform-chain seeds

Exact producer candidates, independent review pending. See PROOF.md.

- Existing n60/MPS120 inputs: gap>=0.0102 for all integer L>=60.
- Smaller n56/MPS112, original cooled-sector recipe: gap>=0.0068 for all integer L>=56.
- Smaller n54/MPS108, generalized direct-sector powers: gap>=0.0025 for all integer L>=54.

Every preceding finite window is checked. No minimum-seed claim and no claim belowL54. New exact MPS contractions took24CPU seconds after a validated benchmark; no new thermal traces or spectra were computed. Reproduce in a disposable copy to preserve sealed timing files.
