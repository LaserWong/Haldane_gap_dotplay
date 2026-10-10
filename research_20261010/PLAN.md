# Research restart — 10 October 2026

## Authorization and scope
The user resumed research from GitHub and requested ongoing main updates and reports every five hours. The confirmed stop time is 13 October 2026, 20:00 America/New_York (14 October 00:00 UTC). A later pause supersedes this schedule.

Baseline: main commit 6be889a30f642bde77fb89af75b3a7379615bed1. GitHub AGENTS.md, README and historical pause records were read. The exported working tree passed all 1,149 original manifest hashes. Historical checkpoint files remain unchanged.

## Active work
1. Independently reconstruct stronger alternating spin-1 chain certificates at g=0.1, 0.125, 0.15. Verify exact local forms, full sparse residuals, completeness and finite-size bridges.
2. Independently reconstruct optimized ordinary-bilayer g=0.01 and g=0.02 inputs and recursion, including finite-size interpolation and short-size bounds.
3. Independently certify the fully frustrated J=0.3 reference with unequal straight/cross couplings, initially epsilon=0.005. Check occupancy counting, star inequalities, exact residuals and all-size scope.
4. Prove and numerically validate a full-low-band residual/completeness method, targeting the ordinary-bilayer g=0.03 ground-only-tail obstruction.

Save new scripts, exact results and reviews in the corresponding subdirectories. Keep rigorous proofs, exact arithmetic, independent checks, floating benchmarks and unverified candidates explicitly separate.

## Resource and verification policy
Use the available cloud filesystem and computation environment. There is no authorized desktop executor or saved cloud coding environment in the current environment catalog. Limit each numerical lane to two CPU cores and about 2 GB RAM, BLAS threads one. Avoid duplicate long runs. Estimate cost and retain checkpoints before extending calculations.

Each published result must state Hamiltonian, normalization, parameters, boundary multiplicities, integer-size scope, full Hilbert dimension, trial dimension, residual/tail certification, executable reproduction command and independent audit status. Do not call a sufficient tested parameter value a maximum.

## Reports and end checkpoint
Regular reports begin 10 October 18:15 EDT and recur every five hours through 13 October 16:15 EDT. At 20:00 EDT on 13 October stop computations, save reproducible results and partial work, update main and report remaining tasks. New work after this deadline requires a further user request.

## Milestone update — 13:46 EDT / 17:46 UTC

The initial three independent audits and all-size bridges are complete. The ordinary bilayer g=.03 now passes the new full-low-band and number-sector-tail route, with independently reviewed all-size gap .009195338283. Stronger chain points through g=.16125 and the specified-method obstruction at .1615 are audited. The FF one-product-state interval through epsilon=.00475 is certified.

Current priorities: larger-seed exact ground moments and translated low band; independent verification of later scalar improvements; interval certificates beyond the existing FF continuum range; bounded spin2 heat benchmarks and error proof. Completed physical audits should be reused rather than rerun without a change. Progress and caveats remain in each result directory and CURRENT_STATUS.json.
