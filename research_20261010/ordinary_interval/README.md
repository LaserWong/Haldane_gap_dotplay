# Closed bilayer intervals from ground-state inputs

Updated 2026-10-10 14:51 America/New_York (EDT) / 18:51 UTC.

Sixteen adjoining closed intervals give a candidate uniform gap bound of 0.001945771244 for 0≤g≤.07 and every integer periodic square side L≥2. Independent review remained pending for this exact calculation.

The retained trace rank is one on each patch. Trial bases are 11/29/29
dimensional on 4x4/8x4/8x8 rungs. The largest patch uses only G/K first moments,
not H2, residuals, excited trials or a complete spectral tail. The two smaller
patches use full residuals plus a parity-refined Temple bound and the complete
quadratic-boson q>=1 reference tail. No new large geometry was computed.

Read `PROOF.md` for the parity argument, concave endpoint bounds, shared-g
energy cancellation, finite reference counting and all-integer bridges.
`coverage_summary.json` links all 16 certificate records. `replay_result.json`
records the completed exact frozen-vector producer replay, without eigensolves.

For reproduction with one CPU, a 1.5 GiB address-space cap, and BLAS threads fixed at one, run

    bash REPRODUCE.sh

The shortest replay runs in a few seconds and changes only replay result/log
files in this directory. To regenerate proposed vectors and the interval cover, run

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/ordinary_interval/certify_intervals.py

That regeneration overwrites candidate interval records. Preserve the handoff
freeze during independent review. At g=0 the exact decoupled gap is 1. The
interval proof also directly includes zero. These sufficient lower bounds do
not identify a physical transition or exclude methods at stronger couplings.

Independent review should check the frozen candidate, particularly parity preservation by the oscillator unitary and the exact interval-endpoint arithmetic.
