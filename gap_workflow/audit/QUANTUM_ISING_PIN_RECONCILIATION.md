# Quantum Ising reviewed-source pin reconciliation

Date: 2026-10-14.

The theory-note authors completed provenance-only corrections requested during independent review. The integration review read the final text and refreshed the two document pins below. No Hamiltonian, parity formula, interval-arithmetic algorithm, K=5 bound, Fourier argument, or finite-size bridge changed. The reviewed mathematical code and independent review report retain their prior hashes.

- theory/QUANTUM_ISING_INTERVAL.md separates transfer eligibility from signed all-integer interpolation and the dedicated K=5 theorem, and corrects deployment-relative links to their source documents.
  - Previous SHA-256: 602803f17409ac6d9d9d265f73a46c40e3927e684aa7334ce2f4d5ebfdcbdc37
  - Current SHA-256: 6f0ba52a47d25bcbef43ccef48abf19af1af0f906e30454726881422cb5bac3a
- theory/QUANTUM_ISING_SEEDS.md replaces stale pending-work language with a certification-follow-through section, links the interval companion and original interpolation/bootstrap sources, and preserves the distinction between numerical candidates and certified companion outputs.
  - Previous SHA-256: bab2df03592cabb69532e26b01e1237770ac6078d6beae0866d8a920764af310
  - Current SHA-256: 42a0724cea8a6f1b4409c69c709b1d596098da596cf0a6aa2ac4dc3b2d340209

Both authors confirmed completion and no further edits before the final integration freeze. The source-integrity guard remains enabled. Future mismatches still block physical certification; this reconciliation does not permit arbitrary refreshes.

The post-reconciliation full test run is recorded in full_suite_20261014_1959.log. Fresh examples are rerun separately rather than reusing certificates from older source fingerprints.
