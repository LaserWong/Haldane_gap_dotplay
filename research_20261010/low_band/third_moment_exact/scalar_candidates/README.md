# Exact all-size candidates and the .10 scan

Updated 2026-10-10 17:10 EDT / 21:10 UTC. Independent acceptance is required.

The ordinary-bilayer g=.09 candidate replays use exactly one largest-seed
numerator state and the unchanged smaller-seed denominator input.

- Exact two-vector upper: candidate all-integer-L≥2 gap 0.001111944974
- Exact 43-dimensional-search upper: candidate gap 0.027330086079

Both variants retain one numerator state. The 43-dimensional search space
is distinct from a retained band of 43 physical states. No new trial residual,
ground lower endpoint, denominator bound, or omitted-state count is asserted.

The denominator snapshots are byte-for-byte copies of the old combined input.
The input_* files retain the old 4×4 and 8×4 objects. Their 8×8 object replaces
the ground upper endpoint with the exact rational trial upper and omits all
old excited numerator contributions. In the txy route the 8×8 seed enters
only the numerator. Its computed upper trace is not used.

Every exact candidate stores its initial rational partition-function ratio
bounds, each repeated raw txy and canonical ladder, the common physical
(n,n,beta) base, all finite windows before the small-defect bootstrap, and
the separate L=2..7 bound valid throughout g≤.1. Explicit edge labels show
that every completed cycle doubles n, m, and the physical inverse temperature.
The coverage record checks that no earlier integer interval is skipped.

The g=.10 files are bounded floating scans only, using the same newly
contracted geometry and the existing .10 denominator data. No successful
point was found on beta=5..20, step .05, for either trial. This does not exclude
other temperatures, different trials, or different recursion routes.

The root producer's run_scalar_candidates.py reproduces these records. The
separate SCALAR_MANIFEST.json freezes these files and records dependency
hashes. PHYSICAL_MANIFEST.json in the parent directory freezes the physical
and .09 Rayleigh inputs independently of scalar claims.
