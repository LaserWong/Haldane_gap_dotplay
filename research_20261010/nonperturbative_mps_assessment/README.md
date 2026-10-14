# Nonperturbative MPS reference states

2026-10-10 15:37 EDT / 19:37 UTC. Producer results, independent review pending.

- [Scope assessment and proofs](ASSESSMENT.md)
- [Exact uniform spin-1 startup screen](uniform_screen.json)
- [Exact AKLT gap, omitted-state counts and transfer obstruction](aklt_certificate.json)
- [Reproduce under one CPU / 1 GiB](REPRODUCE.sh)

The temperature-first input reduction applies algebraically to the uniform
integer-spin Heisenberg chains. I/P/C are seam rotations, not directions.
At n=6/8 the specified single D26 numerator fails for all beta, even with exact
denominator traces. An AKLT D=2 state gives a separate fully counted entangled
reference certificate, but its use in the existing spatial-transfer bootstrap
requires a missing transfer inequality. This calculation did not add a uniform-Heisenberg gap certificate.
