# Accepted independent small-seed exclusion

Updated: 2026-10-10 14:16 America/New_York (EDT, UTC−4) / 18:16 UTC.
Status: complete. Both physical reconstruction and independent all-beta rational replay passed. No computation remains running for this audit.

## Result

For the ordinary spin-1/2 square bilayer with unit rung exchange and straight in-layer exchange **g=0.04 or g=0.05**, the fixed **2×2 → 4×2 → 4×4 canonical x→y→temperature lower-bound recurrence fails at every inverse temperature β≥0, even when started from exact physical traces**.

The proof forces a nonpositive upper enclosure of a recurrence output. It is not a failed sufficient-basin test and does not infer anything from a finite temperature grid. Improving trial precision or retaining more spectral states cannot rescue this unchanged exact-input recurrence. Other seed sizes, axis orders, additional trace injections, recurrence inequalities and proof methods remain open. This does not imply a physical gap closes.

- For 0≤β≤4, physical thermal-purity monotonicity proves failure by update 3 for both couplings.
- For 4≤β≤20, 320 consecutive closed rational boxes per coupling prove failure by update 4 at g=.04 and update 2 at g=.05.
- For β≥20, exact positive energy-curvature slopes and nonnegative relative gaps prove failure by update 2 at g=.04 and update 1 at g=.05.

Thus global failure is certified by at most four updates at g=.04 and three at g=.05. Every intermediate positive-domain requirement is enforced.

## Physical acceptance

All six final coupling-specific complete bands and their number-sector tails were independently reconstructed. The 2×2, 4×2 and 4×4 retained ranks are 13, 25 and 49 in full Hilbert dimensions 256, 65,536 and 4,294,967,296.

Ground search dimensions are 4, 11 and 11; their expanded supports are 34, 1,101 and 20,081, and their reached supports are 38, 4,067 and 452,093. The two largest excited search supports contain 3,936 and 3,376 configurations, each carrying 16 retained trial columns; the M=1 block has an exact spin-flipped partner. These dimensions are separate from retained band rank and are not MPS bond dimensions.

Every full G/A/B/E matrix, residual leakage, rank, Ritz endpoint, Schur endpoint, occupied/empty-edge bound and all 426 positive Jacobi LDL pivots passed exact checks. Counting starts the omitted tail at the correct global ordered index, and every tail multiplicity is included.

On 4×4 the independently verified shifted 50th-eigenvalue cutoffs are 1.775456374051 at g=.04 and 1.697559811076 at g=.05. The g=.05 degeneracy-sensitive corrected M=1 proposal has exact rank 16 and all Ritz upper endpoints at most 1.06957921323. The preserved rejected proposal has a highest Ritz endpoint above the counted cutoff and is not used.

## Scalar checks

A separate 256-bit/70-term rational exponential enclosure was used, importing no producer arithmetic. Every independently computed box input is no greater than its producer upper bound. The producer's coarser inputs were also repropagated independently and force the same failed-update indices.

For g=.04 the middle-box failed-update histogram is 18 / 150 / 70 / 82 at updates 1 / 2 / 3 / 4. For g=.05 it is 149 / 171 at updates 1 / 2. The closest failed upper witnesses to zero are approximately −0.0009107817 and −0.0054346557; these decimals summarize exact rational negative bounds.

At β=4 the independently bounded thermal purities are below 0.287408 for both couplings. The two cold slopes are strictly positive: approximately (0.04077971, 0.04075375) at g=.04 and (0.06467481, 0.06460742) at g=.05.

## Evidence and reproduction

- [Detailed proof and scope](REVIEW.md)
- [Physical exact reconstruction](physical_results.json)
- [Independent all-beta replay and every box](scalar_results.json)
- [Joined acceptance and provenance](ACCEPTANCE.json)
- [Input hashes](SOURCE_MANIFEST_SHA256.json)
- [Audit file hashes](MANIFEST_SHA256.json)

From the repository root, run sequentially:

    PYTHONDONTWRITEBYTECODE=1 python research_20261010/small_seed_exclusion_review/physical_audit.py
    PYTHONDONTWRITEBYTECODE=1 python research_20261010/small_seed_exclusion_review/scalar_audit.py

Both scripts write only this directory and import no producer module. They reuse explicitly hashed, previously independent physical-kernel/inertia or exponential helpers; every present coupling-specific input is freshly recomputed. Each process is constrained to one CPU, one BLAS thread and a 1 GiB address-space limit. The final physical pass took about 259 seconds with 294 MiB peak RSS; the scalar pass took 52 seconds with 35 MiB peak RSS. Times are environment-dependent.

The raw physical stdout file contains interleaved output from a redundant launch of the same audit; both runs completed, shared the same single-CPU affinity, and left identical scientific checks. Runtime/RSS metadata reflect the final complete result. Acceptance depends on the exact result objects and final input-hash verification, not the raw stdout formatting. Producer data and remote state were not modified.
