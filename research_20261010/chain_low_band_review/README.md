# Independent counted low-band review

Updated 10 October 2026, 15:33 EDT (America/New_York) / 19:33 UTC.

## Accepted result

For the periodic spin-one alternating chain, with unit strong exchange and M weak bonds including the two distinct links at M=2, the following lower bounds hold for every integer M>=2. Each finite volume has a unique ground state.

| g | Uniform gap lower bound | Initial beta | Time / canonical cycles | Asymptotic onset M |
|---|---:|---:|---:|---:|
| .18 | .112949677804 | 11.2 | 3 / 0 | 64 |
| .185 | .096048414952 | 11.45 | 3 / 0 | 64 |
| .19 | .078956697835 | 11.75 | 3 / 0 | 64 |
| .195 | .061526095375 | 12.2 | 3 / 1 | 128 |
| .2 | .043446395688 | 12.75 | 3 / 1 | 128 |

These are five discrete sufficient certificates. No interval between the couplings, optimal coupling threshold, actual gap, phase boundary, or infinite-volume ground-state uniqueness is asserted. All five uniform values are limited by the integer window [8,16], rather than the final asymptotic estimate.

## What changed and what was checked

The M=4 denominator has a new counted Hermitian/Schur comparison, proved in `COUNTED_BLOCK_THEOREM.md`. It uses the exact bare vacuum-plus-single-triplet compression and full off-diagonal residual Gram, without assuming that thirteen physical eigenvalues lie below the complement cutoff. At g=.2, nine physical triplet states actually lie above that cutoff; the independent diagnostic explicitly tests this case.

- P has dimension 13 and Q has dimension 6,548, in physical dimension 6,561.
- The complement is selected by weighted strong-dimer energy, with local energies 0,1,3 and multiplicities 1,3,5. All twenty single-quintet states remain in Q at energy 3.
- Every entry of the 13-column Gram, compressed first moment, full second moment and residual Gram is independently reconstructed.
- All five local 81-dimensional positive-definiteness checks, rational root enclosures, root orderings and complete tail counts pass.
- The trace contains exactly one independently certified ground term, triplet multiplicities 3/6/3, and 6,548 remaining ordered-reference terms. No state is dropped or counted twice.
- The old M=4 ground input is checked with the previously sealed independent full-physical-action kernel. The M=8 Rayleigh quotient is evaluated from the previously independently certified two-vector first-moment matrices, whose source seal is checked.
- All 153 saved scalar paths pass, with 801 finite-window checks including the new initial [4,8] window. M=2 and M=3 have direct local bridges. The later windows are contiguous to the all-integer asymptotic onset.
- Nine deliberate corruptions are rejected: normalization, residual off-diagonal, second moment, magnetic degeneracy, quintet omission, tail count, complement cutoff, root direction and ground shift.

The new reference space contains thirteen bare vectors. Their shifted-H action union has 172 configurations; unshifted-H and trial-plus-action union have 173; the residual union has 160. These counts are distinct from the existing 1,099-configuration ground search, its 1,107-configuration full action support, and the M=8 two-vector first-moment combination on 43,294 configurations. The largest full Hilbert space is still 9^8=43,046,721 for sixteen spin-one sites. None of these linear-space or support dimensions is an MPS bond dimension.

## Evidence and reproduction

`audit_certificate.py` imports no producer mathematical module. It uses freshly reconstructed bare-band physics, copies scalar helpers from the sealed independent joint-ratio review, and encloses exponentials with a separate 110-term Taylor calculation at directed 384-bit dyadic precision. It checks the frozen producer package, prior accepted reviews, and external source hashes before acceptance.

- `SUMMARY.json`: all accepted bounds, exact scope, provenance and resource measurements
- `review_g*.json`: complete candidate-path, short-bridge and window replay records
- `block_premises.json`, `verify_blocks.py`: exact independent physical P/Q premises
- `COUNTED_BLOCK_THEOREM.md`: complete comparison, counting, trace and bridge justification
- `physical_diagnostic.json`, `physical_diagnostic.py`: optional complete M=4 physical-basis floating checks, never certificate evidence
- `rejection_guards.json`, `rejection_guards.py`: deliberately corrupted inputs rejected
- `snapshot/`: all 29 frozen producer files, preserved byte-for-byte
- `INPUT_SHA256SUMS.json`: inputs read by the independent full replay
- `MANIFEST_SHA256.json`: sealed review artifacts, excluding itself and Python caches

The reviewed producer manifest SHA-256 is

`2fe7f6300a64381e25bf5d41f19cafec0506a739986ded95784029b40c42470e`.

The inherited independent chain-review manifest SHA-256 is

`0af04a6c84baa0a87c777a5f9e99aad6d5c903821d5ec3e1b21d71ace84684f4`.

Run `REPRODUCE.sh` from any directory. It first verifies the review seal if present, then recomputes in a temporary sibling directory so the frozen review remains unchanged. It replays the exact physics, all candidate paths, negative tests and the optional physical diagnostic. Only the temporary replay directory is removed afterward.

The initial full exact audit took 55.35 seconds and peaked at 27.48 MiB RSS. The standalone full M=4 floating diagnostic took 1.21 seconds and peaked at 66.82 MiB. Each process is pinned to one CPU and capped at 1 GiB address space. These are verification costs, not original search costs. Clean replay details are in `reproduce.log`.

The workspace is an extracted tree without Git metadata; this review changes no predecessor freeze and implies no remote publication. This is an executable exact-arithmetic mathematical certificate, not a proof-assistant formalization.
