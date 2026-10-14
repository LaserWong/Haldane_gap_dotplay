# Independent quadratic-boson comparison review

Updated 2026-10-10 14:32 America/New_York (EDT) / 18:32 UTC.

The independent review verifies the stable quadratic-boson comparison for finite ordinary periodic bilayers with 0≤g<1/4. It includes hard-core min-max compression, directed rational frequency bounds, and the finite reference-tail overcount.

- Complete proof and implementation cautions: [PROOF.md](PROOF.md)
- Acceptance summary: [results/summary.json](results/summary.json)
- All 14 frozen bin replays: [results/bin_replay.json](results/bin_replay.json)
- Exact oscillator factorizations: [results/small_oscillators.json](results/small_oscillators.json)
- Complete 2×2 physical count checks: [results/physical_counts.json](results/physical_counts.json)
- Reproduction: `bash REPRODUCE.sh`

For D=3N, α=1−2g, δ=sqrt(1−4g), and v=(3g²/4)Σ_e w_e², the full ordered spectrum is bounded below by the equal-frequency reference energies −v/(α+δ)+qδ, with multiplicities C(D+q−1,q). At N=64,g=.06, this certifies λ_194(H+48)≥1.546274506411. The exact directed rational endpoint is recorded in the bin replay. It improves the separately reviewed Jacobi tail input 1.368913479949.

These oscillator multiplicities differ from physical triplet-shell multiplicities C(N,q)3^q. The q=2 threshold starts at the same index 2+3N, but higher q indices do not agree. Their labels must not be mixed in a heat-trace calculation. The positive finite sum q=2..N with oscillator multiplicities is a valid overcount because C(4N,N)≥4^N.

The audit checked three exact small-mode factorizations, including negative pairing and a rotated unequal-frequency example. It independently reconstructed all 256 physical states of the 2×2 bilayer at g=.03 and .06. Exact negative counts at the first four thresholds are 0,1,13,67 for both the physical Hamiltonian and its quadratic compression, within the reference allowances 0,1,13,91. The 14 frozen endpoint files all passed.

No new global spectral-gap certificate is claimed. Retained-band enclosures, heat traces, recurrence, and finite-size bridges require separate replay before such a claim. The previous Jacobi review remains unchanged and sealed.

The producer freeze has SHA-256 `ac5c47a1a3ccff0962b7ad5aac3968834b9ff06026644e0abc56601bec750723`. Inputs and review outputs have separate manifests. The audit imports no producer module, changes no producer file, and makes no remote write. It took about 77 seconds, used about 78 MiB peak RSS, and was pinned to one CPU with a 1.5 GiB address-space limit.
