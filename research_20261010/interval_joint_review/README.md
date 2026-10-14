# Interval extension using joint thermal ratios

Updated 2026-10-10 15:25 America/New_York (EDT, UTC−4) / 19:25 UTC.

The independent review accepted two new closed intervals that certify every real 0.078≤g≤0.08 and every integer L≥2 with gap ≥0.008215303694. Joining the unchanged sealed prior cover certifies the entire 0≤g≤0.08 interval with gap ≥0.001945771244 and a unique finite-volume ground state.

- [Full audit and precise scope](REVIEW.md)
- [Machine-readable accepted result](results/SUMMARY.json)
- [Producer and scalar-theorem acceptance gates](ACCEPTANCE_GATES.json)
- [Physical matrix reconstruction](results/physical_polynomials.json)
- [41 certificate-corruption tests](results/adversarial_rejections.json)
- [Reproduction command](REPRODUCE.sh)

The ordinary periodic spin-1/2 square bilayer has unit rung coupling, equal straight intralayer coupling g and no crossed exchange. Length-two bond multiplicities are retained. The largest patch has 128 physical spins and full dimension 2^128. The base trial dimensions are 11/29/29, and the largest filtered augmented dimension is ≤30. Each denominator retains one ground level, and the largest patch supplies one numerator contribution. No odd-band trial inputs are used. The largest complete second moment is required, but no H³/H⁴ or new geometry is used.

The new general lemma is independently sealed in `../joint_ratio_review/LEMMA_REVIEW_MANIFEST.json`. No physical upgrade was made before that acceptance and the producer freeze. All earlier frozen files remain unchanged. No new Git commit or remote publication is claimed.

This sealed result can be included in the project status. Further coupling extensions require their own interval and finite-size audits. The current review makes no claim above g=0.08.
