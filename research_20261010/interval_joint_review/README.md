# Joint-aware interval extension: independent review

Updated 2026-10-10 15:25 America/New_York (EDT, UTC−4) / 19:25 UTC.

Status: PASS. Two new closed intervals certify every real 0.078≤g≤0.08 and every integer L≥2 with gap ≥0.008215303694. Joining the unchanged sealed prior cover certifies the entire 0≤g≤0.08 interval with gap ≥0.001945771244 and a unique finite-volume ground state.

- [Full audit and precise scope](REVIEW.md)
- [Machine-readable accepted result](results/SUMMARY.json)
- [Producer and scalar-theorem acceptance gates](ACCEPTANCE_GATES.json)
- [Physical matrix reconstruction](results/physical_polynomials.json)
- [41 certificate-corruption tests](results/adversarial_rejections.json)
- [Reproduction command](REPRODUCE.sh)

Ordinary periodic spin-1/2 square bilayer; unit rung coupling, equal straight intralayer g, no crossed exchange, length-two bond multiplicity retained. Largest patch: 128 physical spins, full dimension 2^128. Base trial dimensions: 11/29/29; largest filtered augmented dimension ≤30. One retained ground level per denominator and one largest-patch numerator contribution; no odd-band trial inputs. The largest complete second moment is required, but no H³/H⁴ or new geometry is used.

The new general lemma is independently sealed in `../joint_ratio_review/LEMMA_REVIEW_MANIFEST.json`; no physical upgrade was made before that acceptance and the producer freeze. All earlier frozen files remain unchanged. No new Git commit or remote publication is claimed.

Next step: use this sealed exact result in the project status; further coupling extensions require their own interval and finite-size audit. The current review makes no claim above g=0.08.
