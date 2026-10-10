# Extend alternating-chain frontier above 0.2

Updated 2026-10-10 17:28 America/New_York (EDT) / 21:28 UTC.

## Exact producer results

All candidates below have passed complete producer replay and await external independent review. Model: periodic spin-one alternating Heisenberg chain, strong exchange one, weak exchange g, 2M physical spins and all M periodic weak links.

| Discrete g | Gap lower bound for every integer M≥2 | Initial β | Time/canonical cycles | Asymptotic onset |
|---|---:|---:|---:|---:|
| 0.21 | 0.101607534008 | 8.3 | 3 / 0 | M=64 |
| 0.22 | 0.065580452251 | 8.55 | 3 / 1 | M=128 |
| 0.225 | 0.045509923956 | 8.7 | 4 / 1 | M=256 |

Each finite volume has a unique ground state. These are discrete sufficient certificates, not a coupling interval, phase boundary, exact gap, or infinite-volume uniqueness result. All three selected uniform gaps are limited by the first [8,16] window, not the final asymptotic estimate.

The M=4 denominator reference space increased from 13 to 67 bare vectors: every weighted strong-dimer state with E<3. Single quintets retain energy three and stay in the 6,494-dimensional omitted complement. The new exact full action union is 786 configurations; the residual union is 719. These are distinct from the 67-dimensional reference, the full physical dimension 6,561, and the 1,099-dimensional sparse ground trial with 1,107-dimensional full action support.

The maximum physical seed remains M=8 (16 spin-one sites), dimension 43,046,721. Its sealed 43,294-configuration two-vector Rayleigh-only input is unchanged in scope. No larger physical seed, largest-seed residual, or full-spectrum diagonalization is used. None of these dimensions is an MPS bond dimension.

## Method and bottleneck

PROOF.md proves the exact counted partial-spectrum comparison by rational Schur inertia at thresholds below the omitted compression cutoff. It does not assume all 67 physical Ritz levels lie below that cutoff. Every omitted state is counted by (1+3x+5x³)^4. Ground replacement subtracts exactly one ordered comparison contribution.

Every exact candidate includes both direct short M=2,3 bridges, the entire [4,8] integer window, all later contiguous windows, and the terminal all-integer asymptotic theorem. There are 72 saved accepted paths and 378 finite-window checks in producer replay. Independently implemented 384-bit exponential enclosures verify all scalar witnesses.

At g=.25 the present saved physical inputs and specified first time-first/[8,16]-window recipe have an exact all-β obstruction, described in OBSTRUCTION.md. The obstruction caps the recipe's certified ratio lower endpoints, not the physical ratios. It remains fully compatible with a physical gap and with other certification methods. The earlier .21/.22/.225/.25 thirteen-vector failures are only bounded scan results; they are not all-β exclusions.

The next natural input is the 195-dimensional E<4 small reference, including 108 three-triplet states and twenty single quintets at weighted energy three. Keep the maximum M=8 numerator Rayleigh-only and verify full residual, exact counts and all early windows again. A hypothetical numerator sensitivity test is saved, but it does not establish that its requested improved Rayleigh value is physically attainable.

## Files and checks

- PHYSICAL_FREEZE.json: immutable physical inputs and production sources
- SCALAR_FREEZE.json: immutable successful candidate files and scalar source
- expanded_moments.json / expanded_inputs.json: full rational comparison inputs
- candidate_g*.json / summary.json: exact paths, all bridges and selected gaps
- obstruction_g1d4.json / OBSTRUCTION.md: rigorous fixed-recipe all-temperature obstruction
- diagnostic_sensitivity.json: hypothetical-input floating diagnostics only
- verification.json: complete producer exact replay with separate scalar arithmetic
- PRESERVED_PREDECESSOR_SEALS.json / EXTERNAL_INPUT_SHA256.json: verified inherited seals and source hashes
- FROZEN_MANIFEST.json: complete producer package seal
- REPRODUCE.sh: clean sibling replay; does not overwrite the frozen package

All numerical jobs use one allowed CPU, one BLAS thread, and a one-GiB address-space limit. Exact scalar production took 147.86 s and peaked at 78.90 MiB RSS; complete producer replay took 36.90 s and peaked at 27.88 MiB. The compact obstruction proof took 1.91 s. Timings include environmental contention and are not complexity claims.

No root files or prior archives were changed, no Git metadata is present, and no remote publication is implied.
