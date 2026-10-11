# Exact Brauer-rule compiler and checked sample

Frozen 2026-10-11 02:35 UTC / 2026-10-10 22:35 EDT. Producer complete; independent review pending.

N/F/L compile to 634/14532/1941 invariant pairing diagrams, versus 6824/263791/34618 Cartesian matrix units. Total serialized diagrams: 342140 bytes; record/index gate charge: 1596000 bytes, below 16 MiB.

Every local matrix equals the sealed Cartesian reference. Both physical fixtures and all 15 signed moment terms match. Every one of the 512×15 output coefficients for each family equals the Cartesian indexed action: 23040 exact per-channel comparisons.

Brauer action timings for 512 targets are .200126/1.63998/.462633 CPU seconds. Mean scaling to all 169911 origin-containing supports totals 764.181 seconds, or 7641.810 seconds with a tenfold factor, before remaining moment work. This fails the old 180-second proposal, but is not fundamental infeasibility or a prohibition on a separately approved larger budget.

The single executed computation used 20.110278 CPU seconds and 28032 KiB RSS; bounded postprocessing used .084718 CPU seconds. CPU6, one thread, 256 MiB runtime address space; compilation separately at 512 MiB. No full support sweep/cache, full 8×4 moment or new gap claim. No optimization/hardening reruns occurred.

See PROOF.md, run/analysis.json and run/summary.json. The Cartesian predecessor remains sealed unchanged. A complete m3/m4 implementation/cost proposal, rather than production execution, is the next design step.
