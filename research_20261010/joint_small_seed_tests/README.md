# Joint-purity tests with the smaller bilayer seeds

Updated 2026-10-10 17:05 America/New_York (EDT, UTC-4) / 21:05 UTC.

## Result

The saved 2×2 / 4×2 / 4×4-rung inputs did not yield a successful bootstrap at g=.04 or .05 in the tested joint-purity scheme.
The scan explicitly retains partial paths from all six orders, square ratios,
the separate full ratio, and same-base mixed-order transport. It does not discard
an unfinished order's valid partial bounds or reuse K at the wrong basepoint.

- Bounded diagnostic: beta=1 through 60, spacing 1/40, 2,361 points per coupling.
  The scan uses at most 16 complete cycles and 16 closure sweeps per cube, with no successful proposal.
- Directed rational replay: eight selected points, using saved physical low-band
  and full-tail endpoints. At g=.04 the best grid point beta=337/40 gives a first
  doubled-base joint lower bound about .324447952058220 and next G output
  about -1.167691924568251. At g=.05 no full first-cycle joint survives the grid.
- New candidate all-beta result: a position-wise cap invariant dominates all
  allowed same-base mixed transports and preserved square/full products. It passes
  640 closed temperature boxes plus the hot/cold rays. This stronger conclusion
  awaits a separate analytic review. It is not inherited from the older fixed-order
  exclusion.

The all-beta scope is the explicitly specified synchronous mixed-cube scalar
algorithm, even with exact initial physical traces. It does not exclude fresh
trace injections, nonsynchronous reordering at other bases, different scalar
inequalities, or every possible use of this physical seed. No claim of the
mathematically minimum seed across all methods is warranted.

## Files and reproducibility

- PROOF.md: exact method, new cap invariant, all-beta candidate, and scope
- scan_joint_small.py / results.json: bounded scan and exact selected traces
- certify_envelope.py / envelope_results.json: new all-beta upper envelopes
- verify_envelope_records.py / record_verification.json: a second exact arithmetic
  replay of all 644 envelope records. This is distinct from acceptance by a separate analyst
- MANIFEST_SHA256.json: package seal, excluding itself

Run the three Python scripts from the repository root. Each writes this directory
only and uses one pinned CPU with a 1 GiB address-space cap. The final diagnostic
run took about 9.7 seconds and 13 MiB RSS. The envelope construction took about 1.2
seconds and 24 MiB RSS. Timings depend on concurrent load. Physical reconstruction
is inherited from the accepted small_seed_exclusion_review. No new physical
support, vector, full ED, frozen/root edit, or remote write is made.

The maximum physical seed remains 16 rungs / 32 spins / Hilbert dimension 2^32.
Its retained low band has 49 states, and its saved ground search space has
dimension 11. These are distinct notions of dimension.

No successful candidate exists in these records, so no new all-integer-L gap,
short-size bridge, or finite-window certificate is claimed.
