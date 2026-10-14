# Independent uniform-gap certificate at every periodic length

Updated October 11, 2026, at 02:51 UTC / October 10, 2026, at 22:51 America/New_York.

The unit-bilinear periodic spin-1 Heisenberg chain has an independently accepted unique ground state and gap≥.0023 for every integer L≥2.
Both periodic bonds are counted at L = 2.
Bootstrap initialization remains 30.

The exact proof combines analytic bounds at lengths 2 and 3, fresh own-length MPS and direct thermal bounds at 4..23, and the accepted tail from 24.
All 40 new integers, 14 signed polynomial majorants, and 20 finite inequalities passed review.
The stronger nested bounds remain .0179 from length 28, .0245 from 32, and .0248 from 34.
No minimum-size claim is made.

The guarded physical run used 4.279 s of elapsed time, 4.213 s of wait4 CPU time, 4.208 s of program CPU time, and 8.3 MiB.
Post-exec limits and a single thread on CPU 5 were verified.
The separate historical resource anomaly in the direct length-25 calculation remains unresolved.

`PROOF.md`, `results.json`, and `guard_resources.json` give the proof and records.
Run `python audit.py` in a disposable copy for the inexpensive replay.
Do not bypass the physical launcher's no-retry record.
