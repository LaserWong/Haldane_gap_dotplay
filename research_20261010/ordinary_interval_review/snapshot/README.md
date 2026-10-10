# Ordinary bilayer: closed coupling intervals, ground-only inputs

Updated 2026-10-10 14:51 America/New_York (EDT) / 18:51 UTC.

**Exact candidate, pending independent review.** Sixteen adjoining closed
intervals cover the entire 0<=g<=.07 range and give a common gap lower bound
0.001945771244 for every integer periodic square side L>=2.

The retained trace rank is one on each patch. Trial bases are 11/29/29
dimensional on 4x4/8x4/8x8 rungs. The largest patch uses only G/K first moments,
not H2, residuals, excited trials or a complete spectral tail. The two smaller
patches use full residuals plus a parity-refined Temple bound and the complete
quadratic-boson q>=1 reference tail. No new large geometry was computed.

Read `PROOF.md` for the parity argument, concave endpoint bounds, shared-g
energy cancellation, finite reference counting and all-integer bridges.
`coverage_summary.json` links all 16 certificate records. `replay_result.json`
records the completed exact frozen-vector producer replay, without eigensolves.

Reproduction (one CPU, 1.5 GiB address-space cap, BLAS threads fixed at one):

    bash REPRODUCE.sh

The shortest replay runs in a few seconds and changes only replay result/log
files in this directory. To regenerate proposed vectors and the interval cover:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python research_20261010/ordinary_interval/certify_intervals.py

That regeneration overwrites candidate interval records. Preserve the handoff
freeze during independent review. At g=0 the exact decoupled gap is 1; the
interval proof also directly includes zero. These sufficient lower bounds do
not identify a physical transition or exclude methods at stronger couplings.

Next action: independently review the frozen candidate, especially parity
preservation of the oscillator unitary and exact continuous endpoint arithmetic.
