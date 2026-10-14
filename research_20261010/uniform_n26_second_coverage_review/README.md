# Accepted parity-resolved coverage from 26

Updated 2026-10-11 02:32 UTC /2026-10-10 22:32 America/New_York.

The unit-bilinear spin-one Heisenberg chain has a unique ground state and a certified gap≥.0023 for every integer periodic L≥26. New exact proofs cover 26 and 27 individually. They join the accepted tail from 28. Bootstrap initialization remains 30.

Stronger bounds remain .0179 from 28, .0245 from 32 and .0248 from 34. No minimum-size claim or claim below 26 is made.

See PROOF.md and results.json. The proof independently derives the parity-sensitive interpolation, validates the previously freshly rebuilt physical MPS52, and reproduces the failed simplified full-window bound without turning it into an obstruction.

Replay in a disposable copy with the pinned sibling packages by running python audit.py. The hard caps are 60 CPU seconds and 256 MiB on CPU 4. Actual usage was .163 CPU seconds and 14.8 MiB. No contractions or thermal jobs are launched.
