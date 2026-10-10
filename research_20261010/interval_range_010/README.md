# Extend the continuous ordinary bilayer interval to .10

Updated 2026-10-10 17:56 America/New_York (EDT) / 21:56 UTC.
Exact producer result; independent interval review required.

Ten closed intervals cover every real g in [.09,.10] and every integer L>=2
with unique ground state and gap >= .008761649092. Joining accepted [0,.09]
preserves gap >= .001945771244 on [0,.10] (66 intervals total).

The only strengthened physical input is the accepted complete 8x4-rung fixed
witness residual polynomial. Other bands/tails and the one-state 43D largest
numerator use their valid coupling-dependent inputs. Search dimensions are
11,43,43, retained denominator counts 49,97, and numerator count one. Largest
Hilbert dimension is 2^128. No physical-gap monotonicity is assumed.

Read PHYSICAL_PROOF.md and SCALAR_PROOF.md. Exact records include every
joint basepoint, 46 finite windows, 60 L=2,...,7 checks and analytic tails.
replay_result.json records exact eigensolver-free replay and eleven corruption
tests. PHYSICAL_MANIFEST.json, SCALAR_MANIFEST.json and FROZEN_MANIFEST.json
bind the immutable package, with explicit accepted input/review hashes.

From the repository root: bash research_20261010/interval_range_010/REPRODUCE.sh
This verifies hashes and recomputes all scalar certificates without overwriting
frozen results. Generation and replay use CPU5, one numerical-library thread
and a 1 GiB address-space cap; each takes roughly ten seconds and <90 MiB.
All writes are confined here. Prior seals, root files and GitHub are untouched.
