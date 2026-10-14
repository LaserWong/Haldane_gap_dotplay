# Exact Brauer-rule compiler

The compiler reproduces the sealed Cartesian reference for every local matrix, both physical fixtures, and all 15 signed moment terms. Its output was frozen on 2026-10-11 at 02:35 UTC / 2026-10-10 at 22:35 EDT. Independent review was pending at that time.

The N/F/L families contain 634/14532/1941 invariant pairing diagrams, compared with 6824/263791/34618 Cartesian matrix units. The serialized diagrams occupy 342140 bytes. The record/index charge is 1596000 bytes, below the 16 MiB limit. For each family, all 512×15 output coefficients agree with the Cartesian indexed action, giving 23040 exact per-channel comparisons.

For 512 targets, the three Brauer actions took .200126/1.63998/.462633 CPU seconds. Scaling their mean times to all 169911 origin-containing supports gives 764.181 seconds, or 7641.810 seconds after applying a tenfold factor, before the remaining moment calculation. This estimate exceeds the earlier 180-second proposal. It does not establish fundamental infeasibility, and a larger budget would require separate approval.

The executed calculation used 20.110278 CPU seconds and 28032 KiB RSS. Bounded postprocessing used .084718 CPU seconds. Execution used CPU6, one thread, and a 256 MiB address-space limit. Compilation had a separate 512 MiB limit. No full support sweep, cache, complete 8×4 moment, or new gap result was produced. No optimization or hardening rerun was performed.

`PROOF.md`, `run/analysis.json`, and `run/summary.json` contain the derivation and outputs. The Cartesian predecessor remains unchanged. The next step is a complete m3/m4 implementation and cost proposal before considering production execution.
