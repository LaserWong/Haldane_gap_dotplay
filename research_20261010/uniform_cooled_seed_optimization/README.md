# Cooled seeds for the uniform chain

The exact producer calculations give three candidate bounds, pending independent review. `PROOF.md` gives the argument and assumptions.

- Existing n60/MPS120 inputs give gap≥0.0102 for every integer L≥60.
- The smaller n56/MPS112 construction uses the original cooled-sector recipe and gives gap≥0.0068 for every integer L≥56.
- The n54/MPS108 construction uses generalized direct-sector powers and gives gap≥0.0025 for every integer L≥54.

Every preceding finite window is checked. The results establish neither coverage below L54 nor a minimum seed size. New exact MPS contractions used 24 CPU seconds after a validated benchmark. No new thermal traces or spectra were computed. Reproduce in a disposable copy to preserve the sealed timing records.
