# Exact third moment and enlarged numerator candidate

Updated 2026-10-10 17:12 EDT / 21:12 UTC. Independent review pending.

The additional contraction is inexpensive and improves the ordinary-bilayer
g=9/100 numerator. No q≥8 states were constructed. Old data and denominator
lower bounds were not changed.

| Geometry | Exact residual Rayleigh | Exact two-vector shifted upper | Enlarged search rank | Enlarged shifted upper |
|---|---:|---:|---:|---:|
| 4×4 | 5.576709347473 | −0.102078999223 | 16 | −0.102080672818 |
| 8×4 | 5.631896214986 | −0.203816392144 | 43 | −0.203851429570 |
| 8×8 | 5.652811915402 | −0.406262328876 | 43 | −0.406785348394 |

The 8×8 enlarged rational shifted upper is exactly

    −31428158707615927910605435473378 / 77259809950543885422866334827335.

At maximum size there are 64 rungs, 128 physical spins, and full Hilbert
dimension 2^128. The search dimension is 43; one trial state is retained.
The original search dimension was 29. The two-vector filter plane has at
most two dimensions, independently of these search dimensions.

## Validation and resources

- Every F/S/V/W/X/Y/Z entry agrees between full matching, fixed-origin
  matching, and explicit sparse physical action on 2×2, 4×2, and 4×4.
- An additional B+L fixture agrees exactly in H′, H′², and H′³ on all three.
- All large-size old F/S/V/W entries reproduce their previously saved values.
- All base moments M0..M4 reproduce in the enlarged Hankel construction;
  exact M5 is exported and exact Gram rank is checked.
- Microbenchmark: 20,000 uniformly spaced 8×8 q6 targets, 0.134 s contraction,
  1.18 s setup; 7.84 s linear full projection, 78.4 s with a 10× margin.
- Full 8×8: 992,424 q6 targets, 6.81 s elapsed, 119.7 MiB peak RSS.
- Hard execution limits: one pinned CPU, 1 GiB address space, 600 CPU seconds,
  610 s wall timeout. The pre-run 600 CPU-second/700 MiB gate passed.

The largest stored physical test support is the 4×4 fixture, 451,389 states
after one H′ action, at 70.8 MiB process RSS. Production 8×8 uses only a q4
matching cache and a q6 mask list, with no physical sparse state storage.

## Scalar diagnostic and exact candidates

Using only the improved 8×8 numerator and keeping smaller seeds and all
denominator input unchanged, a bounded β=7..14 step .05 txy screen gives:

- Two-vector: 6 successful grid points; best diagnostic score 0.00113987 at β=8.9
- Enlarged search: 61 grid points; best diagnostic score 0.0273424 at β=8.75

Those initial floating scores kept the old odd numerator terms. The separate
exact replay in `scalar_candidates/` retains only the new single ground
numerator state and now supplies all-integer-L≥2 candidate lower bounds:

- Two-vector: 0.001111944974, β=8.9; all early windows through 2048 included
- Enlarged: 0.027330086079, β=8.75; all early windows through 128 included

The short L=2..7 bridge, each physical temperature/base and ladder label, and
the terminal bootstrap are saved. These exact candidate results still require
independent audit before being called certified gap bounds.

The same geometry supplies g=.10 largest-seed shifted Rayleigh uppers
−0.503327958199 (two-vector) and −0.504442728941 (43-dimensional search).
Neither produces a successful floating point on the bounded β=5..20 step .05
screen with unchanged .10 denominators. This is not an all-temperature exclusion.

## Files and next step

- `DERIVATION.md`: normalization, contraction, moment, and enlarged-basis formulas
- `contract_third.cpp`: reusable exact geometry producer
- `test_physical.cpp`, `physical_local_A.*`: independent sparse physical fixtures
- `fixture_tests.json`: exact fixture and translation checks
- `benchmark_gate.json`, `full_8x8.log`: gated resource evidence
- `geometry_*_origin.json`: exact F/S/V/W/X/Y/Z
- `filtered_*_g9d100.json`: rational two-vector pencil and selected filter
- `enlarged_*_g9d100.json`: rational enlarged trial and exact base M5
- `scalar_diagnostic.json`: bounded floating candidate only
- `scalar_candidates/`: exact .09 all-size candidates, unchanged denominator
  snapshots, explicit ladder/window labels, and bounded .10 diagnostics
- `PHYSICAL_MANIFEST.json`, `scalar_candidates/SCALAR_MANIFEST.json`:
  separate immutable physical and scalar-input seals for independent review
- `REPRODUCE.sh`: isolated replay in a fresh output directory

Next: independently audit both the contractions/trial data and the exact
scalar/all-size candidates. No GitHub or root
status files were edited by this worker.
