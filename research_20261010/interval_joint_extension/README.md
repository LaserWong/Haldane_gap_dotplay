# Complete the continuous ordinary-bilayer interval through .08

Updated 2026-10-10 15:20 America/New_York (EDT, UTC−4) / 19:20 UTC.

Exact candidate, pending the independent joint-lemma and interval audits.
Two closed intervals [.078,.079] and [.079,.08] give gap≥.008215303694 for all
integer square sides L≥2. Together with the unchanged sealed earlier packages,
33 pieces cover the full 0≤g≤.08 range at gap≥.001945771244.

- [Proof, partition, and new scalar dependency](PROOF.md)
- [Exact interval ledger](coverage_summary.json)
- [All-size replay and combined union](replay_result.json)
- [Physical polynomial verification](source_validation.json)
- [Uniform filter tests](test_results.json)
- [Joint arithmetic diagnostics](joint_test_results.json)

There is one ground contribution on each patch and no odd-band trial input.
Original search dimensions are 11/29/29; the used augmented dimensions are
11/29/≤30, with q≤6 for the implicit largest filtered vector. Existing full
second moments are used, with no H³/H⁴ or new physical contraction.
The largest physical Hilbert space has dimension 2^128.

Reproduce from the repository root:

    bash research_20261010/interval_joint_extension/REPRODUCE.sh

The sealed .078 result retains its independent, older-scalar status. This
separate .08 variant uses the new joint-product propagation and interpolation.
